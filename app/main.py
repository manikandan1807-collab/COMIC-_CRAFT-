"""
main.py

ComicCraft application entry point. Run with:

    uvicorn app.main:app --reload

Then visit http://127.0.0.1:8000
"""

import os

from dotenv import load_dotenv

# Load environment variables (GEMINI_API_KEY, HF_API_KEY) before anything
# that reads them at import time.
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router

app = FastAPI(
    title="ComicCraft",
    description="AI Comic Story Creator using Gemini Models + Stable Diffusion",
    version="1.0.0",
)

# Ensure the static output directories exist before mounting
for folder in ("static/panels", "static/exports", "static/fonts"):
    os.makedirs(folder, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)
