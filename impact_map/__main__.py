"""Brain Function Impact Map command line.

Usage:
    python -m impact_map path/to/mri.jpg [--view axial|coronal|sagittal] [--lang en|hi] [--ai-explain]
"""

import argparse
import json
import os

from .predictor import load_classifier, load_image, predict_with_gradcam
from .report import analyze, render_figure, render_markdown


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("image", help="path to an MRI image")
    parser.add_argument("--view", default="axial", choices=["axial", "coronal", "sagittal"],
                        help="slice orientation of the image (default: axial)")
    parser.add_argument("--lang", default="en", choices=["en", "hi"], help="report language")
    parser.add_argument("--model-dir", default="models", help="folder with brain_tumor_vgg16.keras and classes.json")
    parser.add_argument("--out-dir", default="impact_reports", help="where to write the figure and reports")
    parser.add_argument("--ai-explain", action="store_true",
                        help="also write a family-friendly explanation with Claude (needs ANTHROPIC_API_KEY)")
    args = parser.parse_args()

    model, classes = load_classifier(args.model_dir)
    image = load_image(args.image)
    probabilities, cam = predict_with_gradcam(model, classes, image)
    result = analyze(image, probabilities, cam, args.view)

    os.makedirs(args.out_dir, exist_ok=True)
    stem = os.path.join(args.out_dir, os.path.splitext(os.path.basename(args.image))[0])
    render_figure(image, cam, result, stem + "_impact_map.png")
    with open(stem + "_impact_map.json", "w") as f:
        json.dump(result, f, indent=2)
    report = render_markdown(result, args.lang)

    if args.ai_explain and result["tumor_detected"]:
        from .explain import explain_with_claude
        explanation = explain_with_claude(result, args.lang)
        if explanation:
            report += "\n---\n\n## AI explanation for the family\n\n" + explanation + "\n"

    with open(stem + f"_impact_map_{args.lang}.md", "w", encoding="utf-8") as f:
        f.write(report)
    print(report)
    print(f"Saved figure and reports to {args.out_dir}/")


if __name__ == "__main__":
    main()
