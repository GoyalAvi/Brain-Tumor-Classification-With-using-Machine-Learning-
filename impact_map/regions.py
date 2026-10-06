"""Approximate mapping from 2D MRI slice positions to brain regions.

This is a rough geometric atlas, not true image registration. The brain is
segmented from the background, its bounding box is normalised to [-1, 1] on
both axes, and each pixel is assigned to a region by simple rules for the
chosen slice view. Accurate mapping needs 3D scans registered to a real atlas
(for example MNI space); treat every result here as "approximately".

Display conventions assumed (standard radiological display):
  axial:    anterior (front of head) at the top, patient's right on image left
  coronal:  superior (top of head) at the top, patient's right on image left
  sagittal: anterior on image left, superior at the top
"""

import cv2
import numpy as np

VIEWS = ("axial", "coronal", "sagittal")

# Region ids, in the order used for the colour-coded region map.
REGION_IDS = ("frontal", "parietal", "temporal", "occipital", "frontoparietal",
              "deep", "sellar", "cerebellum_brainstem")


def brain_mask(image):
    """Segment the head from the dark background and return a filled boolean mask."""
    gray = image if image.ndim == 2 else cv2.cvtColor((image * 255).astype("uint8"), cv2.COLOR_BGR2GRAY)
    if gray.dtype != np.uint8:
        gray = (gray * 255).astype("uint8")
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8), iterations=2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(gray)
    if contours:
        cv2.drawContours(mask, [max(contours, key=cv2.contourArea)], -1, 255, thickness=cv2.FILLED)
    return mask > 0


def normalised_coords(mask):
    """Per-pixel coordinates scaled so the brain's bounding box spans [-1, 1]."""
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        raise ValueError("Could not find the brain in the image")
    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    half_w, half_h = max((xs.max() - xs.min()) / 2, 1), max((ys.max() - ys.min()) / 2, 1)
    yy, xx = np.mgrid[0:mask.shape[0], 0:mask.shape[1]]
    return (xx - cx) / half_w, (yy - cy) / half_h


def region_label_map(mask, view):
    """Return an int array: -1 outside the brain, else an index into REGION_IDS."""
    if view not in VIEWS:
        raise ValueError(f"view must be one of {VIEWS}")
    nx, ny = normalised_coords(mask)
    labels = np.full(mask.shape, -1, dtype=int)
    rules = _RULES[view](nx, ny)
    assigned = np.zeros(mask.shape, dtype=bool)
    for region, condition in rules:  # first matching rule wins
        hit = condition & mask & ~assigned
        labels[hit] = REGION_IDS.index(region)
        assigned |= hit
    return labels


def _axial_rules(nx, ny):
    r = np.hypot(nx, ny)
    return [
        ("deep", r < 0.3),
        ("frontal", ny < -0.25),
        ("occipital", ny > 0.55),
        ("temporal", np.abs(nx) > 0.65),
        ("parietal", np.ones_like(nx, dtype=bool)),
    ]


def _coronal_rules(nx, ny):
    return [
        ("sellar", (np.abs(nx) < 0.18) & (ny > 0.3) & (ny < 0.65)),
        ("cerebellum_brainstem", (np.abs(nx) < 0.3) & (ny >= 0.65)),
        ("deep", (np.abs(nx) < 0.35) & (np.abs(ny) < 0.3)),
        ("temporal", ny > 0.2),
        ("frontoparietal", np.ones_like(nx, dtype=bool)),
    ]


def _sagittal_rules(nx, ny):
    return [
        ("cerebellum_brainstem", (ny > 0.45) & (nx > 0.1)),
        ("sellar", (np.abs(nx) < 0.15) & (ny > 0.2) & (ny <= 0.5)),
        ("deep", np.hypot(nx, ny) < 0.25),
        ("frontal", (nx < -0.2) & (ny < 0.25)),
        ("occipital", nx > 0.5),
        ("temporal", ny > 0.15),
        ("parietal", np.ones_like(nx, dtype=bool)),
    ]


_RULES = {"axial": _axial_rules, "coronal": _coronal_rules, "sagittal": _sagittal_rules}


def locate_hotspot(cam, mask, view, threshold=0.5):
    """Summarise where the Grad-CAM attention falls inside the brain.

    Returns a dict with the peak point, the patient side, and the share of
    attention falling in each region (largest first).
    """
    labels = region_label_map(mask, view)
    attention = np.where(mask & (cam >= threshold), cam, 0.0)
    total = attention.sum()
    if total == 0:
        return {"regions": [], "side": None, "peak_xy": None, "attention_inside_brain": 0.0}

    shares = []
    for index, region in enumerate(REGION_IDS):
        share = float(attention[labels == index].sum() / total)
        if share > 0:
            shares.append({"region": region, "share": round(share, 3)})
    shares.sort(key=lambda s: s["share"], reverse=True)

    yy, xx = np.mgrid[0:cam.shape[0], 0:cam.shape[1]]
    peak_x, peak_y = (attention * xx).sum() / total, (attention * yy).sum() / total  # attention centroid
    nx, _ = normalised_coords(mask)
    side = None
    if view in ("axial", "coronal"):
        # Radiological convention: image left is the patient's right.
        weighted_x = float((attention * nx).sum() / total)
        side = "midline" if abs(weighted_x) < 0.15 else ("right" if weighted_x < 0 else "left")

    inside = float(np.where(mask, cam, 0).sum() / max(cam.sum(), 1e-8))
    return {"regions": shares, "side": side, "peak_xy": [int(peak_x), int(peak_y)],
            "attention_inside_brain": round(inside, 3)}
