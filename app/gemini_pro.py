"""
gemini_pro.py

Uses Google's Gemini Pro model to expand a panel-by-panel outline into a full
comic-style story, complete with narration and character dialogue.
"""

import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini Pro: optimized for detailed, creative text generation
model = genai.GenerativeModel("gemini-1.5-pro")


def generate_story(outline: list) -> str:
    """
    Generates a detailed comic story with narration and character dialogue
    from a list of comic panel outlines using Gemini Pro.

    Args:
        outline (list): A list of dicts, one per panel (from generate_outline()).

    Returns:
        str: The generated comic story text, with each panel's section marked
             by "**Panel N" so it can be split back apart programmatically.
    """
    # Format the panel outline as a numbered list for clarity
    formatted_outline = "\n".join(
        [
            f"{i + 1}. {panel.get('title', 'Untitled')}: {panel.get('scene_description', '')}"
            for i, panel in enumerate(outline)
        ]
    )

    prompt = f"""
You're a comic book writer.

Given the following panel breakdown, write a comic-style story with engaging narration and character dialogues for each panel.

Panel Outline:
{formatted_outline}

Guidelines:
- Use a fun and engaging tone, like an actual comic book.
- Include narration and clearly marked character lines (e.g., CHARACTER: "line").
- Keep each panel self-contained but part of a cohesive story.
- Begin each panel's section with the exact marker "**Panel {{N}}" (e.g. "**Panel 1") so the
  output can be reliably split panel-by-panel afterwards.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Unexpected error generating story:", e)
        return f"Error generating story: {str(e)}"
