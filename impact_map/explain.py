"""Optional: ask Claude to turn the structured result into a family-friendly explanation.

Needs `pip install anthropic` and an ANTHROPIC_API_KEY. The explanation is
grounded only in the JSON result and the region knowledge base.
"""

import json

from .knowledge import REGIONS

SYSTEM_PROMPT = """You explain the output of an educational brain-MRI research tool to a patient's family.
Rules:
- This is NOT a diagnosis. Say so clearly, once, in a calm way.
- Use only the facts in the provided JSON and region notes. Do not invent tumor type, size, grade or prognosis.
- The region location is approximate; if location_uncertain is true, say the location is uncertain.
- Use simple words, short paragraphs, and end with practical next steps (see a neurologist or neurosurgeon,
  bring the scans, note any symptoms). Mention urgent care for sudden severe headache, seizure, loss of
  consciousness, sudden weakness or vision loss.
- Write in the requested language."""


def explain_with_claude(result, lang="en"):
    import anthropic

    language = {"en": "English", "hi": "Hindi"}[lang]
    region_notes = {r["region"]: {k: v["en"] for k, v in REGIONS[r["region"]].items()}
                    for r in result.get("regions", [])}
    client = anthropic.Anthropic()
    response = client.beta.messages.create(
        model="claude-opus-5-5",
        max_tokens=4000,
        output_config={"effort": "low"},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": (
            f"Language: {language}\n\nResult:\n{json.dumps(result, indent=2)}\n\n"
            f"Region notes:\n{json.dumps(region_notes, indent=2)}")}],
    )
    if response.stop_reason == "refusal":
        return None
    return "".join(block.text for block in response.content if block.type == "text").strip()
