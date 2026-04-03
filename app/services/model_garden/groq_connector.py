import os
import time
import logging
from typing import Dict, Optional

from groq import Groq
from dotenv import load_dotenv
from requests.exceptions import ConnectionError as NetworkError

from .base_connector import BaseModelConnector, ModelConnectorException
from .config_schema import ModelConfig

load_dotenv()

logger = logging.getLogger(__name__)


class GroqConnector(BaseModelConnector):
    """
    Production-grade Groq connector.
    Supports structured validation similar to OpenAIConnector.
    """

    # Groq currently supports text models only
    TEXT_MODELS = {
        "llama-3.3-70b-versatile",
        "mixtral-8x7b-32768",
        "qwen2.5-32b-instruct"
    }

    VISION_MODELS = set()  # No official vision support yet
    AUDIO_MODELS = set()   # No official audio support yet

    def __init__(self, model_name: str, max_retries: int = 3):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ModelConnectorException("GROQ_API_KEY not set.")

        self.client = Groq(api_key=api_key)
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

        # 🔒 Capability validation
        if image_url and self.model_name not in self.VISION_MODELS:
            raise ModelConnectorException(
                f"Model '{self.model_name}' does not support vision processing."
            )

        if (audio_url or audio_base64 or voice) and self.model_name not in self.AUDIO_MODELS:
            raise ModelConnectorException(
                f"Model '{self.model_name}' does not support audio processing."
            )

        if not prompt:
            raise ModelConnectorException("Prompt is required for Groq text models.")

        attempt = 0

        while attempt < self.max_retries:
            try:
                messages = [
                    {"role": "user", "content": prompt}
                ]

                api_args = {
                    "model": self.model_name,
                    "messages": messages,
                    "temperature": config.temperature,
                    "top_p": config.top_p,
                    "max_tokens": config.max_tokens,
                }

                response = self.client.chat.completions.create(**api_args)

                message = response.choices[0].message
                content = message.content

                if content is None:
                    content = ""

                return {
                    "response": str(content),
                    "audio": None,
                    "id": str(response.id)
                }

            except NetworkError:
                logger.warning("Network error. Retrying...")
                time.sleep(2 ** attempt)

            except Exception as e:
                logger.exception("Groq API error")
                raise ModelConnectorException(
                    f"Groq generation failed: {str(e)}"
                ) from e

            attempt += 1

        raise ModelConnectorException("Max retries exceeded. Groq model unavailable.")