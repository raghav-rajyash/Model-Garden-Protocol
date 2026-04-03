from typing import Dict
from app.services.model_garden.base_connector import BaseModelConnector


class ModelGarden:

    def __init__(self):
        self._registry: Dict[str, BaseModelConnector] = {}

    def register(self, name: str, connector: BaseModelConnector):
        self._registry[name] = connector

    def get(self, name: str) -> BaseModelConnector:
        if name not in self._registry:
            raise ValueError(f"Model '{name}' is not registered.")
        return self._registry[name]



model_garden = ModelGarden()
