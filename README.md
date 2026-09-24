# ComicCraft - AI Comic Story Creator

Turn a story prompt into a fully illustrated, downloadable comic using
Google's Gemini models (story) and Stable Diffusion (illustrations).

## 1. Setup

```bash
# From the comiccraft/ folder

python -m venv env

# Windows
env\Scripts\activate
# macOS / Linux
source env/bin/activate

pip install -r requirements.txt
```

## 2. Add your API keys

Copy `.env.example` to `.env` and fill in your real keys:

```bash
cp .env.example .env
```

```
GEMINI_API_KEY=your_gemini_api_key_here
HF_API_KEY=your_huggingface_api_key_here
```

- Get a Gemini API key: https://ai.google.dev/
- Get a Hugging Face token (needs access to `runwayml/stable-diffusion-v1-5`):
  https://huggingface.co/settings/tokens

## 3. Run the app

```bash
uvicorn app.main:app --reload
```

Then open:
- App: http://127.0.0.1:8000
- Interactive API docs: http://127.0.0.1:8000/docs

## 4. How it works

1. You fill out the form on the homepage (story prompt, character name,
   setting, tone, art style).
2. **Gemini Flash** turns your prompt into a structured 5-panel outline.
3. **Gemini Pro** expands the outline into full narration and dialogue.
4. **Stable Diffusion** generates an illustration for each panel.
5. Everything is assembled into a preview page and an exportable PDF.

## 5. Project structure

```
comiccraft/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── routes.py            # All API/page routes
│   ├── gemini_flash.py      # Panel outline generation
│   ├── gemini_pro.py        # Narration & dialogue generation
│   ├── image_generator.py   # Stable Diffusion image generation
│   ├── layout_builder.py    # Combines text + images into a layout
│   └── exporters.py         # PDF export (FPDF)
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
├── static/
│   ├── panels/               # Generated panel images
│   ├── exports/               # Exported comic PDFs
│   └── fonts/
├── requirements.txt
└── .env.example
```

## Notes

- First run will download the Stable Diffusion model (a few GB) — this
  requires network access and may take a while.
- If you don't have a GPU, image generation will run on CPU and be slower.
- `/generate-comic/json` accepts the same inputs as JSON for programmatic use:

```json
{
  "prompt": "A brave fox exploring an enchanted forest.",
  "character_name": "Finn",
  "setting": "forest",
  "tone": "dramatic",
  "style": "anime"
}
```
