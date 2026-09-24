"""
routes.py

Defines all FastAPI routes for ComicCraft:
- "/"                     -> homepage / input form
- "/generate"              -> form-based comic generation -> HTML preview
- "/generate-comic/json"   -> JSON-based comic generation -> JSON response
- "/export-success"        -> confirmation page after PDF download
- "/test-image"            -> standalone image-generation test utility
"""

import traceback

from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf

router = APIRouter()
templates = Jinja2Templates(directory="templates")


class PromptRequest(BaseModel):
    """Schema for JSON-based comic generation requests."""
    prompt: str
    character_name: str
    setting: str
    tone: str
    style: str


def _build_full_prompt(prompt: str, character_name: str, setting: str, tone: str, style: str) -> str:
    """Combines all user inputs into a single descriptive prompt for the outline model."""
    return (
        f"{prompt}\n"
        f"The main character is {character_name}. "
        f"The setting is a {setting}. "
        f"The tone is {tone}. The art style is {style}."
    )


def _run_comic_pipeline(full_prompt: str) -> tuple[list, str]:
    """
    Runs the full ComicCraft generation pipeline:
    outline -> story -> images -> layout -> PDF.

    Returns:
        tuple: (layout, pdf_path)
    """
    # Step 1: Generate panel outline
    outline = generate_outline(full_prompt)

    if not isinstance(outline, list) or not all("image_prompt" in panel for panel in outline):
        raise ValueError("Invalid outline structure from Gemini response.")

    # Step 2: Generate story narration/dialogue
    full_story = generate_story(outline)

    # Step 3: Generate images, one per panel
    images = [generate_image(panel["image_prompt"]) for panel in outline]

    # Step 4: Build layout
    layout = build_comic_layout(images, full_story, outline)

    # Step 5: Export to PDF
    pdf_path = save_pdf(layout)

    return layout, pdf_path


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Loads the homepage with the story input form."""
    return templates.TemplateResponse(request=request, name="index.html")


@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    style: str = Form(...),
):
    """Handles form submission: generates the comic and renders the preview page."""
    try:
        full_prompt = _build_full_prompt(prompt, character_name, setting, tone, style)
        layout, pdf_path = _run_comic_pipeline(full_prompt)

        # Make the path safe/usable for the web (served from /static)
        web_pdf_path = "/" + pdf_path.replace("\\", "/")

        return templates.TemplateResponse(
            "comic_preview.html",
            {
                "request": request,
                "layout": layout,
                "pdf_path": web_pdf_path,
            },
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-comic/json")
async def generate_comic_json(payload: PromptRequest):
    """API route: accepts a JSON payload, generates the comic, returns JSON."""
    try:
        full_prompt = _build_full_prompt(
            payload.prompt, payload.character_name, payload.setting, payload.tone, payload.style
        )
        layout, pdf_path = _run_comic_pipeline(full_prompt)

        web_pdf_path = "/" + pdf_path.replace("\\", "/")

        return JSONResponse(
            content={
                "layout": layout,
                "pdf_path": web_pdf_path,
            }
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf_path: str):
    """Displays a confirmation page after the comic PDF has been downloaded."""
    return templates.TemplateResponse(
        "export_success.html",
        {
            "request": request,
            "pdf_path": pdf_path,
        },
    )


@router.get("/test-image")
async def test_image(prompt: str = "A futuristic city at sunset, sci-fi, cinematic, artstation"):
    """Developer utility: tests image generation directly from a prompt."""
    try:
        image_path = generate_image(prompt)
        return {"message": "Image generated successfully", "path": image_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
