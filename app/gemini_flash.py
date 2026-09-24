"""
gemini_flash.py

Uses Google's Gemini Flash model to generate a structured, panel-by-panel
comic outline from a user's story prompt.
"""

import os
import json
import google.generativeai as genai

# Configure the Gemini client with the API key from environment variables
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini Flash: optimized for fast, structured output
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_outline(user_prompt: str) -> list:
    """
    Generates a 5-panel comic layout based on the user's story idea using Gemini.

    Args:
        user_prompt (str): The user's comic idea prompt.

    Returns:
        list: A list of dictionaries, one for each panel, each containing:
              "panel", "title", "scene_description", "image_prompt".
              On failure, returns a single-item list with an "error" key.
    """
    prompt = f"""
You are a professional AI comic planner.

Your task is to generate a *strictly formatted* JSON array containing 5 panel descriptions for a comic based on the story idea below:

STORY: "{user_prompt}"

Each JSON object must include:
- "panel" (integer)
- "title" (string)
- "scene_description" (string)
- "image_prompt" (string)

Respond ONLY in this valid JSON format, without any explanations or markdown:
[
  {{
    "panel": 1,
    "title": "Title here",
    "scene_description": "Scene description here",
    "image_prompt": "Image prompt for Stable Diffusion"
  }},
  ...
]
"""

    try:
        response = model.generate_content(prompt)
        output_text = response.text.strip()

        # Remove markdown code fences if Gemini adds them despite instructions
        if output_text.startswith("```json"):
            output_text = output_text.replace("```json", "").replace("```", "").strip()
        elif output_text.startswith("```"):
            output_text = output_text.replace("```", "").strip()

        panel_data = json.loads(output_text)

        # Validate structure
        if not isinstance(panel_data, list):
            raise ValueError("Gemini response is not a list.")

        for panel in panel_data:
            if not isinstance(panel, dict) or not all(
                key in panel for key in ("panel", "title", "scene_description", "image_prompt")
            ):
                raise ValueError(f"Invalid panel format or missing keys: {panel}")

        return panel_data

    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        print("Full text received:\n", output_text if "output_text" in locals() else "")
        return [{"error": f"JSON parsing failed: {str(e)}"}]

    except Exception as e:
        print("Unexpected error generating outline:", e)
        return [{"error": f"Generation failed: {str(e)}"}]
