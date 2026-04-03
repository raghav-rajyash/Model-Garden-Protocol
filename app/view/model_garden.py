from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.model_garden.model_garden import model_garden
from app.services.model_garden.config_schema import ModelConfig


router = APIRouter(
    prefix="/api/v1/model",
    tags=["Model Garden"]
)


# ✅ REQUEST MODEL
class GenerateRequest(BaseModel):
    model: str
    prompt: Optional[str] = None
    config: ModelConfig
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    audio_base64: Optional[str] = None
    voice: Optional[str] = None


# ✅ RESPONSE MODEL
class GenerateResponse(BaseModel):
    response: Optional[str] = None
    audio: Optional[str] = None
    id: Optional[str] = None


@router.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):

    try:
        model = model_garden.get(request.model)

        result = model.generate(
            prompt=request.prompt,
            config=request.config,
            image_url=request.image_url,
            audio_url=request.audio_url,
            audio_base64=request.audio_base64,
            voice=request.voice
        )

        return GenerateResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))