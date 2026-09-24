"""
layout_builder.py

Combines the generated panel images and the full comic story text into a
single structured layout, ready for preview rendering or PDF export.
"""


def build_comic_layout(image_paths: list, full_story: str, outline: list) -> list:
    """
    Organizes generated images and the full comic story into a structured layout.

    Args:
        image_paths (list): List of file paths for each panel's generated image.
        full_story (str): The full comic narration/dialogue text from Gemini Pro,
                           with sections marked by "**Panel N".
        outline (list): The original panel outline (from generate_outline()).

    Returns:
        list: A list of dicts, one per panel, each containing:
              "panel", "title", "image_path", "text", "scene_description".
    """
    # Split the full story into individual panel segments
    story_panels = full_story.split("**Panel")
    story_panels = [f"**Panel{panel}" for panel in story_panels if panel.strip()]

    layout = []
    for idx, (image, text, panel_info) in enumerate(
        zip(image_paths, story_panels, outline), start=1
    ):
        layout.append(
            {
                "panel": idx,
                "title": panel_info.get("title", f"Panel {idx}"),
                "image_path": image,
                # Strip the "**Panel N" marker line, keep the rest of the text
                "text": "\n".join(text.strip().splitlines()[1:]).strip(),
                "scene_description": panel_info.get("scene_description", ""),
            }
        )

    return layout
