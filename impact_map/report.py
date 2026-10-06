"""Turn a prediction + Grad-CAM heatmap into a region analysis, a figure and a text report."""

import cv2
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

from .knowledge import REGIONS, SIDE_NOTES, TEXT  # noqa: E402
from .regions import REGION_IDS, brain_mask, locate_hotspot, region_label_map  # noqa: E402

REGION_COLORS = {
    "frontal": "#4e79a7", "parietal": "#59a14f", "temporal": "#f28e2b", "occipital": "#b07aa1",
    "frontoparietal": "#76b7b2", "deep": "#e15759", "sellar": "#edc948", "cerebellum_brainstem": "#9c755f",
}


def analyze(image, probabilities, cam, view, tumor_threshold=0.5):
    """Combine the classifier output and heatmap into a structured result."""
    tumor_prob = probabilities.get("yes", 0.0)
    result = {"view": view, "tumor_probability": round(tumor_prob, 4), "tumor_detected": tumor_prob >= tumor_threshold}
    if not result["tumor_detected"]:
        return result

    location = locate_hotspot(cam, brain_mask(image), view)
    result.update(location)
    top_share = location["regions"][0]["share"] if location["regions"] else 0.0
    result["location_uncertain"] = location["attention_inside_brain"] < 0.7 or top_share < 0.4
    return result


def render_markdown(result, lang="en"):
    t = lambda key: TEXT[key][lang]  # noqa: E731
    lines = [f"# {t('title')}", "", f"> {t('disclaimer')}", "",
             f"**{t('tumor_prob')}:** {result['tumor_probability'] * 100:.1f}%  ", f"**View:** {result['view']}", ""]
    if not result["tumor_detected"]:
        lines.append(t("no_tumor"))
        return "\n".join(lines) + "\n"
    if not result["regions"]:
        lines.append(t("low_confidence"))
        return "\n".join(lines) + "\n"

    top = REGIONS[result["regions"][0]["region"]]
    lines += [f"## {t('likely_region')}: {top['name'][lang]} ({result['regions'][0]['share'] * 100:.0f}%)", ""]
    if result.get("side"):
        lines += [SIDE_NOTES[result["side"]][lang], ""]
    lines += [f"### {t('functions')}"] + [f"- {f}" for f in top["functions"][lang]] + [""]
    lines += [f"### {t('symptoms')}"] + [f"- {s}" for s in top["symptoms"][lang]] + [""]

    others = [r for r in result["regions"][1:] if r["share"] >= 0.15]
    if others:
        lines += [f"### {t('also_involved')}"]
        lines += [f"- {REGIONS[r['region']]['name'][lang]} ({r['share'] * 100:.0f}%)" for r in others] + [""]
    if result.get("location_uncertain"):
        lines += [f"⚠️ {t('low_confidence')}", ""]
    return "\n".join(lines) + "\n"


def render_figure(image, cam, result, out_path):
    """Save a 3-panel figure: original scan, Grad-CAM overlay, labelled region map."""
    rgb = cv2.cvtColor((image * 255).astype("uint8"), cv2.COLOR_BGR2RGB)
    heat = cv2.cvtColor(cv2.applyColorMap((cam * 255).astype("uint8"), cv2.COLORMAP_JET), cv2.COLOR_BGR2RGB)
    overlay = cv2.addWeighted(rgb, 0.6, heat, 0.4, 0)

    panels = 3 if result["tumor_detected"] else 2
    fig, axes = plt.subplots(1, panels, figsize=(5 * panels, 5.4))
    axes[0].imshow(rgb)
    axes[0].set_title("MRI scan")
    axes[1].imshow(overlay)
    axes[1].set_title(f"Model attention (tumor prob {result['tumor_probability'] * 100:.0f}%)")

    if result["tumor_detected"]:
        labels = region_label_map(brain_mask(image), result["view"])
        colored = np.zeros((*labels.shape, 3))
        present = []
        for index, region in enumerate(REGION_IDS):
            if (labels == index).any():
                colored[labels == index] = matplotlib.colors.to_rgb(REGION_COLORS[region])
                present.append(region)
        axes[2].imshow(rgb)
        axes[2].imshow(colored, alpha=0.45)
        if result.get("peak_xy"):
            axes[2].plot(*result["peak_xy"], marker="x", color="white", markersize=14, mew=3)
        top = REGIONS[result["regions"][0]["region"]]["name"]["en"] if result.get("regions") else "unknown"
        side = f" ({result['side']} side)" if result.get("side") else ""
        axes[2].set_title(f"Approx. region: {top}{side}", fontsize=10)
        axes[2].legend(handles=[Patch(color=REGION_COLORS[r], label=REGIONS[r]["name"]["en"].split(" (")[0])
                                for r in present], loc="lower center", bbox_to_anchor=(0.5, -0.32),
                       ncol=2, fontsize=8, frameon=False)

    for ax in axes:
        ax.axis("off")
    fig.tight_layout()
    fig.text(0.01, 0.01, "Brain Function Impact Map - educational use only, not a diagnosis. "
             "Region is approximate.", fontsize=9, color="#555555")
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
