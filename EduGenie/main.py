from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from schemas import InputRequest
from explanation_module import explain_topic
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie - AI Learning Assistant",
    description="A lightweight educational assistant powered by Google Gemini.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "gemini_configured": bool(settings.gemini_api_key),
        "model": settings.gemini_model,
        "mode": "gemini" if settings.gemini_api_key else "demo/offline",
    }


@app.post("/qa")
async def qa(payload: InputRequest):
    try:
        return {"result": answer_question(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/explain")
async def explain(payload: InputRequest):
    try:
        return {"result": explain_topic(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/quiz")
async def quiz(payload: InputRequest):
    try:
        return generate_quiz(payload.text)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/summarize")
async def summarize(payload: InputRequest):
    try:
        return {"result": summarize_text(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/learn/recommendations")
async def recommendations(payload: InputRequest):
    try:
        return {"result": get_learning_recommendations(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
