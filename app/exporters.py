"""
exporters.py

Compiles the finished comic (images + narration) into a downloadable,
multi-page PDF file using FPDF.
"""

import os
from datetime import datetime

from fpdf import FPDF


def save_pdf(layout: list, output_dir: str = "static/exports") -> str:
    """
    Compiles the full comic into a multi-page PDF file.

    Each panel's image and narration are placed on their own page.

    Args:
        layout (list): The structured comic layout from build_comic_layout().
        output_dir (str): Directory to save the exported PDF into.

    Returns:
        str: The file path of the saved PDF.
    """
    os.makedirs(output_dir, exist_ok=True)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()

        # Panel title
        pdf.set_font("Helvetica", "B", 16)
        pdf.multi_cell(0, 10, f"Panel {panel['panel']}: {panel.get('title', '')}")
        pdf.ln(2)

        # Panel image
        image_path = panel.get("image_path")
        if image_path and os.path.exists(image_path):
            try:
                pdf.image(image_path, w=170)
                pdf.ln(5)
            except Exception as e:
                print(f"Could not embed image for panel {panel['panel']}: {e}")

        # Scene description (italic)
        scene_description = panel.get("scene_description", "")
        if scene_description:
            pdf.set_font("Helvetica", "I", 11)
            pdf.multi_cell(0, 7, scene_description)
            pdf.ln(2)

        # Narration / dialogue
        text = panel.get("text", "")
        if text:
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 7, text)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"comic_{timestamp}.pdf"
    filepath = os.path.join(output_dir, filename)
    pdf.output(filepath)

    return filepath
