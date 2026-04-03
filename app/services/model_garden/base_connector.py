from abc import ABC, abstractmethod
from typing import Dict, Optional


class ModelConnectorException(Exception):
    """Base exception for model connector errors."""
    pass


class BaseModelConnector(ABC):

    @abstractmethod
    def generate(
        self, 
        prompt: Optional[str], 
        config: Dict, 
        image_url: Optional[str] = None,
        audio_url: Optional[str] = None,
        audio_base64: Optional[str] = None,
        voice: Optional[str] = None
    ) -> Dict:
        pass
