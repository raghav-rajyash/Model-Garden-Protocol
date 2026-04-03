import os
import time
import logging
from typing import Dict, Optional, List

from openai import OpenAI
from openai import APIError, RateLimitError, APITimeoutError
from requests.exceptions import ConnectionError as NetworkError

from .base_connector import BaseModelConnector, ModelConnectorException
from dotenv import load_dotenv

from .config_schema import ModelConfig

load_dotenv()

logger = logging.getLogger(__name__)


class OpenAIConnector(BaseModelConnector):
    VISION_MODELS = {"gpt-4o", "gpt-4o-mini"}
    AUDIO_MODELS = {"gpt-4o", "gpt-4o-mini", "gpt-4o-audio-preview"}

    def __init__(self, model_name: str, max_retries: int = 3):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_name = model_name
        self.max_retries = max_retries

    def generate(
        self, 
        prompt: Optional[str], 
        config: ModelConfig, 
        image_url: Optional[str] = None,
        audio_url: Optional[str] = None,
        audio_base64: Optional[str] = None,
        voice: Optional[str] = None
    ) -> Dict:

        if image_url and self.model_name not in self.VISION_MODELS:
            raise ModelConnectorException(
                f"Model '{self.model_name}' does not support vision processing."
            )
            
        if (audio_url or audio_base64 or voice) and self.model_name not in self.AUDIO_MODELS:
            raise ModelConnectorException(
                f"Model '{self.model_name}' does not support audio processing."
            )

        attempt = 0
        while attempt < self.max_retries:
            try:
                content: List[Dict] = []
                if prompt:
                    content.append({"type": "text", "text": prompt})
                
                if image_url:
                    content.append({
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    })

                if audio_base64:
                    # Expecting base64 string. Default format to wav if not known
                    content.append({
                        "type": "input_audio",
                        "input_audio": {
                            "data": audio_base64,
                            "format": "wav"
                        }
                    })
                elif audio_url:
                    # For now, we recommend users send audio_base64 for direct input
                    # If it's a URL, some models might need pre-processing or downloading
                    # But for "big company" feel, we try to pass it if supported
                    pass

                api_args = {
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": content}],
                    "temperature": config.temperature,
                    "top_p": config.top_p,
                    "max_tokens": config.max_tokens,
                    "frequency_penalty": config.frequency_penalty,
                    "presence_penalty": config.presence_penalty,
                    "seed": config.seed,
                }

                if voice:
                    api_args["modalities"] = ["text", "audio"]
                    api_args["audio"] = {"voice": voice, "format": "wav"}

                if config.stop:
                    stop_sequences = [s for s in config.stop if s]
                    if stop_sequences:
                        api_args["stop"] = stop_sequences

                response = self.client.chat.completions.create(**api_args)
                message = response.choices[0].message

                result = {
                    "text": message.content,
                }

                if hasattr(message, "audio") and message.audio:
                    result["audio_base64"] = message.audio.data
                    result["id"] = message.audio.id
                    # If content is None, the transcript is usually inside the audio object
                    if not result["text"] and hasattr(message.audio, "transcript"):
                        result["text"] = message.audio.transcript

                return result

            except RateLimitError as e:
                logger.warning("Rate limit exceeded. Retrying...")
                time.sleep(2 ** attempt)

            except APITimeoutError as e:
                logger.warning("API timeout. Retrying...")
                time.sleep(2 ** attempt)

            except NetworkError as e:
                logger.warning("Network issue. Retrying...")
                time.sleep(2 ** attempt)

            except APIError as e:
                logger.error(f"OpenAI API error: {e}")
                raise ModelConnectorException(f"AI Provider Error: {e.message}") from e

            except Exception as e:
                logger.exception("Unexpected error occurred")
                raise ModelConnectorException("Unexpected model error") from e

            attempt += 1

        raise ModelConnectorException("Max retries exceeded. Model unavailable.")
