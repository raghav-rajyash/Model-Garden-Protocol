from .model_garden import model_garden
from .groq_connector import GroqConnector


def register_default_models():
    """
    Registers only Qwen model via Groq.
    """

    model_garden.register(
        "llama-3.3-70b-versatile",
        GroqConnector(model_name="llama-3.3-70b-versatile")
    )