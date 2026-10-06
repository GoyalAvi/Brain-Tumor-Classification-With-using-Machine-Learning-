import json
import subprocess
import sys

import cv2
import numpy as np
import pytest

from impact_map.regions import REGION_IDS, brain_mask, locate_hotspot, region_label_map
from impact_map.report import analyze, render_markdown

SIZE = 224


def synthetic_scan():
    """A grey ellipse 'head' on a black background, as a float BGR image in [0, 1]."""
    image = np.zeros((SIZE, SIZE, 3), np.uint8)
    cv2.ellipse(image, (112, 112), (80, 95), 0, 0, 360, (120, 120, 120), -1)
    return image.astype("float32") / 255.0


def blob_cam(x, y, radius=12):
    cam = np.zeros((SIZE, SIZE), np.float32)
    cv2.circle(cam, (x, y), radius, 1.0, -1)
    return cam


def test_brain_mask_finds_the_head():
    mask = brain_mask(synthetic_scan())
    assert mask[112, 112] and not mask[5, 5]
    assert 0.4 < mask.mean() < 0.6


@pytest.mark.parametrize("view", ["axial", "coronal", "sagittal"])
def test_every_brain_pixel_gets_a_region(view):
    mask = brain_mask(synthetic_scan())
    labels = region_label_map(mask, view)
    assert (labels[mask] >= 0).all()
    assert (labels[~mask] == -1).all()


@pytest.mark.parametrize("view, xy, region, side", [
    ("axial", (150, 40), "frontal", "left"),      # front of head, image right = patient's left
    ("axial", (112, 195), "occipital", None),
    ("axial", (40, 112), "temporal", "right"),
    ("axial", (112, 112), "deep", "midline"),
    ("coronal", (112, 165), "sellar", "midline"),
    ("sagittal", (140, 180), "cerebellum_brainstem", None),
    ("sagittal", (60, 60), "frontal", None),
])
def test_hotspot_lands_in_expected_region(view, xy, region, side):
    image = synthetic_scan()
    result = locate_hotspot(blob_cam(*xy, radius=8), brain_mask(image), view)
    assert result["regions"][0]["region"] == region
    if side:
        assert result["side"] == side
    assert result["attention_inside_brain"] == pytest.approx(1.0)


def test_no_tumor_skips_mapping():
    image = synthetic_scan()
    result = analyze(image, {"no": 0.9, "yes": 0.1}, blob_cam(150, 40), "axial")
    assert result["tumor_detected"] is False
    assert "did not detect" in render_markdown(result, "en")


@pytest.mark.parametrize("lang", ["en", "hi"])
def test_report_mentions_region(lang):
    result = analyze(synthetic_scan(), {"no": 0.1, "yes": 0.9}, blob_cam(150, 40), "axial")
    report = render_markdown(result, lang)
    assert ("Frontal lobe" if lang == "en" else "फ्रंटल लोब") in report
    assert result["location_uncertain"] is False


def test_attention_outside_brain_is_flagged_uncertain():
    result = analyze(synthetic_scan(), {"no": 0.1, "yes": 0.9}, blob_cam(8, 8, radius=30) + 0.6 * blob_cam(150, 40),
                     "axial")
    assert result["location_uncertain"] is True


def test_cli_end_to_end(tmp_path):
    tf = pytest.importorskip("tensorflow")
    inputs = tf.keras.Input((SIZE, SIZE, 3))
    x = tf.keras.layers.Conv2D(4, 3, activation="relu")(inputs)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    model = tf.keras.Model(inputs, tf.keras.layers.Dense(2, activation="softmax")(x))
    model_dir = tmp_path / "models"
    model_dir.mkdir()
    model.save(model_dir / "brain_tumor_vgg16.keras")
    (model_dir / "classes.json").write_text(json.dumps(["no", "yes"]))
    scan = tmp_path / "scan.png"
    cv2.imwrite(str(scan), (synthetic_scan() * 255).astype("uint8"))

    out_dir = tmp_path / "out"
    subprocess.run([sys.executable, "-m", "impact_map", str(scan), "--model-dir", str(model_dir),
                    "--out-dir", str(out_dir), "--lang", "hi"], check=True)
    assert (out_dir / "scan_impact_map.png").exists()
    assert (out_dir / "scan_impact_map_hi.md").exists()
    result = json.loads((out_dir / "scan_impact_map.json").read_text())
    assert set(result) >= {"tumor_probability", "tumor_detected", "view"}
    assert all(r["region"] in REGION_IDS for r in result.get("regions", []))
