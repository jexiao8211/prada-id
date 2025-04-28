from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

import numpy as np
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
from sklearn.decomposition import PCA

# TODO: Use any of these?
class FeatureExtractor(ABC):
    """Base class for feature extraction methods."""
    
    @abstractmethod
    def extract(self, image: Union[Image.Image, np.ndarray]) -> np.ndarray:
        """Extract features from the input image."""
        pass


class ColorHistogramExtractor(FeatureExtractor):
    """Extract color histogram features from images."""
    
    def __init__(self, bins: int = 32):
        self.bins = bins
    
    def extract(self, image: Union[Image.Image, np.ndarray]) -> np.ndarray:
        # Convert PIL Image to numpy array if needed
        if isinstance(image, Image.Image):
            img_array = np.array(image)
        else:
            img_array = image
        
        # Calculate histogram for each color channel
        histograms = []
        for i in range(3):  # RGB channels
            hist = cv2.calcHist([img_array], [i], None, [self.bins], [0, 256])
            hist = cv2.normalize(hist, hist).flatten()
            histograms.extend(hist)
        
        return np.array(histograms)


class ResNetFeatureExtractor(FeatureExtractor):
    """Extract features using a pre-trained ResNet model."""
    
    def __init__(self, model_name: str = "resnet50", layer: str = "avgpool"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load_model(model_name)
        self.layer = layer
        self.transform = transforms.Compose([
            # transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def _load_model(self, model_name: str) -> nn.Module:
        if model_name == "resnet50":
            model = models.resnet50(pretrained=True)
        elif model_name == "resnet101":
            model = models.resnet101(pretrained=True)
        else:
            raise ValueError(f"Unsupported model: {model_name}")
        
        # Remove the final classification layer
        model = nn.Sequential(*list(model.children())[:-1])
        model = model.to(self.device)
        model.eval()
        return model
    
    def extract(self, image: Union[Image.Image, np.ndarray]) -> np.ndarray:
        # Convert numpy array to PIL Image if needed
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        image = image.convert('RGB')

        # Preprocess image
        img_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        # Extract features
        with torch.no_grad():
            features = self.model(img_tensor)
        
        # Flatten features
        features = features.squeeze().cpu().numpy()
        return features


class PCAFeatureExtractor(FeatureExtractor):
    """Apply PCA to reduce dimensionality of features."""
    
    def __init__(self, base_extractor: FeatureExtractor, n_components: int = 100):
        self.base_extractor = base_extractor
        self.n_components = n_components
        self.pca = PCA(n_components=n_components)
        self.is_fitted = False
    
    def fit(self, images: List[Union[Image.Image, np.ndarray]]) -> None:
        """Fit PCA on a list of images."""
        features = [self.base_extractor.extract(img) for img in images]
        features = np.array(features)
        self.pca.fit(features)
        self.is_fitted = True
    
    def extract(self, image: Union[Image.Image, np.ndarray]) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("PCA extractor must be fitted before use")
        
        features = self.base_extractor.extract(image)
        return self.pca.transform(features.reshape(1, -1)).flatten()


class FeatureExtractionPipeline:
    """A pipeline that applies multiple feature extraction methods."""
    
    def __init__(self, extractors: List[FeatureExtractor]):
        self.extractors = extractors
    
    def extract(self, image: Union[Image.Image, np.ndarray]) -> np.ndarray:
        features = []
        for extractor in self.extractors:
            features.extend(extractor.extract(image))
        return np.array(features) 