from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import torch
import torch.nn as nn


class BaseModel(ABC):
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load_model() if model_path else self._create_model()

    @abstractmethod
    def _create_model(self) -> nn.Module:
        """Create and return a new model instance."""
        pass

    @abstractmethod
    def _load_model(self) -> nn.Module:
        """Load a model from the specified path."""
        pass

    @abstractmethod
    def preprocess_image(self, image: Any) -> torch.Tensor:
        """Preprocess the input image."""
        pass

    @abstractmethod
    def predict(self, image: Any) -> Dict[str, Any]:
        """Make a prediction on the input image."""
        pass

    @abstractmethod
    def train(self, train_data: Any, val_data: Any) -> Dict[str, float]:
        """Train the model on the provided data."""
        pass

    def save(self, path: str) -> None:
        """Save the model to the specified path."""
        torch.save(self.model.state_dict(), path)

    def load(self, path: str) -> None:
        """Load the model from the specified path."""
        self.model.load_state_dict(torch.load(path))
        self.model_path = path 