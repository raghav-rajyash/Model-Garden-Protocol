from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.model_garden.model_garden import model_garden
from app.services.model_garden.config_schema import ModelConfig


# ✅ FIXED PREFIX (IMPORTANT)
router = APIRouter(
    prefix="/model",
    tags=["Model Garden"]
)


# =========================
# REQUEST MODEL
# =========================
class GenerateRequest(BaseModel):
    model: str
    prompt: Optional[str] = None
    config: ModelConfig
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    audio_base64: Optional[str] = None
    voice: Optional[str] = None


# =========================
# RESPONSE MODEL
# =========================
class GenerateResponse(BaseModel):
    response: Optional[str] = None
    audio: Optional[str] = None
    id: Optional[str] = None


# =========================
# GENERATE ENDPOINT
# =========================
@router.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    try:
        # Get model from registry
        model = model_garden.get(request.model)

        # Call model
        result = model.generate(
            prompt=request.prompt,
            config=request.config,
            image_url=request.image_url,
            audio_url=request.audio_url,
            audio_base64=request.audio_base64,
            voice=request.voice
        )

        # Debug print (optional)
        print("MODEL RESULT:", result)

        # Safe return
        return {
            "response": result.get("response") or result.get("text"),
            "audio": result.get("audio"),
            "id": result.get("id")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))