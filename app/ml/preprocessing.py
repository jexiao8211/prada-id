from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

import cv2
import numpy as np
from PIL import Image


class ImagePreprocessor(ABC):
    """Base class for image preprocessing steps."""
    
    @abstractmethod
    def process(self, image: Union[Image.Image, np.ndarray]) -> Union[Image.Image, np.ndarray]:
        """Process the input image and return the processed image."""
        pass


class ResizePreprocessor(ImagePreprocessor):
    """Resize images to a standard size."""
    
    def __init__(self, target_size: tuple = (224, 224)):
        self.target_size = target_size
    
    def process(self, image: Union[Image.Image, np.ndarray]) -> Union[Image.Image, np.ndarray]:
        if isinstance(image, Image.Image):
            return image.resize(self.target_size, Image.LANCZOS)
        else:
            return cv2.resize(image, self.target_size)


class BackgroundRemovalPreprocessor(ImagePreprocessor):
    """Remove background from clothing images using the autodistilled yolov8-seg model."""
    
    def __init__(self, threshold: int = 127):
        self.threshold = threshold
    
    # TODO: add imput for clothing type?
    def process(self, image: Union[Image.Image, np.ndarray]) -> Union[Image.Image, np.ndarray]:
        # Convert PIL Image to numpy array if needed
        if isinstance(image, Image.Image):
            img_array = np.array(image)
        else:
            img_array = image.copy()
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # TODO: Apply model to create mask
        _, mask = cv2.threshold(gray, self.threshold, 255, cv2.THRESH_BINARY_INV)
        
        # Apply mask to original image
        result = cv2.bitwise_and(img_array, img_array, mask=mask)
        
        # Convert back to PIL Image if input was PIL Image
        if isinstance(image, Image.Image):
            return Image.fromarray(result)
        return result


class NormalizePreprocessor(ImagePreprocessor):
    """Normalize image pixel values."""
    
    def __init__(self, mean: List[float] = [0.485, 0.456, 0.406], 
                 std: List[float] = [0.229, 0.224, 0.225]):
        self.mean = np.array(mean)
        self.std = np.array(std)
    
    def process(self, image: Union[Image.Image, np.ndarray]) -> Union[Image.Image, np.ndarray]:
        # Convert PIL Image to numpy array if needed
        if isinstance(image, Image.Image):
            img_array = np.array(image).astype(np.float32) / 255.0
        else:
            img_array = image.astype(np.float32) / 255.0
        
        # Normalize
        img_array = (img_array - self.mean) / self.std
        
        # Convert back to PIL Image if input was PIL Image
        if isinstance(image, Image.Image):
            return Image.fromarray((img_array * 255).astype(np.uint8))
        return img_array


class PreprocessingPipeline:
    """A pipeline that applies multiple preprocessing steps in sequence."""
    
    def __init__(self, preprocessors: List[ImagePreprocessor]):
        self.preprocessors = preprocessors
    
    def process(self, image: Union[Image.Image, np.ndarray]) -> Union[Image.Image, np.ndarray]:
        result = image
        for preprocessor in self.preprocessors:
            result = preprocessor.process(result)
        return result 