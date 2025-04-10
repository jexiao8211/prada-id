from typing import Any, Dict, List, Optional, Union

import numpy as np
from PIL import Image

from app.ml.classifiers import Classifier, NearestNeighborClassifier, ClusteringClassifier, EnsembleClassifier
from app.ml.feature_extraction import FeatureExtractor, ResNetFeatureExtractor, PCAFeatureExtractor
from app.ml.preprocessing import ImagePreprocessor, ResizePreprocessor, BackgroundRemovalPreprocessor, NormalizePreprocessor, PreprocessingPipeline


class PradaClassificationPipeline:
    """Main pipeline for Prada clothing classification."""
    
    def __init__(
        self,
        preprocessors: Optional[List[ImagePreprocessor]] = None,
        feature_extractors: Optional[List[FeatureExtractor]] = None,
        classifier: Optional[Classifier] = None,
    ):
        # Default preprocessors
        if preprocessors is None:
            preprocessors = [
                ResizePreprocessor(target_size=(224, 224)),
                BackgroundRemovalPreprocessor(),
                NormalizePreprocessor()
            ]
        
        # Default feature extractors
        if feature_extractors is None:
            feature_extractors = [
                ResNetFeatureExtractor(model_name="resnet50")
            ]
        
        # Default classifier
        if classifier is None:
            classifier = NearestNeighborClassifier(n_neighbors=5)
        
        self.preprocessing_pipeline = PreprocessingPipeline(preprocessors)
        self.feature_extractors = feature_extractors
        self.classifier = classifier
        self.is_fitted = False
    
    def fit(self, images: List[Union[Image.Image, np.ndarray]], labels: List[str]) -> None:
        """Fit the pipeline on training data."""
        # Preprocess images
        processed_images = [self.preprocessing_pipeline.process(img) for img in images]
        
        # Extract features
        features_list = []
        for extractor in self.feature_extractors:
            if isinstance(extractor, PCAFeatureExtractor):
                # PCA extractor needs to be fitted first
                extractor.fit(processed_images)
            
            extractor_features = [extractor.extract(img) for img in processed_images]
            features_list.append(np.array(extractor_features))
        
        # Combine features
        features = np.hstack(features_list)
        
        # Fit classifier
        self.classifier.fit(features, labels)
        self.is_fitted = True
    
    def predict(self, image: Union[Image.Image, np.ndarray]) -> Dict[str, Any]:
        """Make a prediction on a single image."""
        if not self.is_fitted:
            raise ValueError("Pipeline must be fitted before use")
        
        # Preprocess image
        processed_image = self.preprocessing_pipeline.process(image)
        
        # Extract features
        features_list = []
        for extractor in self.feature_extractors:
            features = extractor.extract(processed_image)
            features_list.append(features)
        
        # Combine features
        features = np.hstack(features_list)
        
        # Make prediction
        result = self.classifier.predict(features)
        
        return result
    
    def update(self, new_images: List[Union[Image.Image, np.ndarray]], new_labels: List[str]) -> None:
        """Update the model with new data."""
        if not self.is_fitted:
            self.fit(new_images, new_labels)
            return
        
        # For nearest neighbor classifier, we can simply add new data
        if isinstance(self.classifier, NearestNeighborClassifier):
            # Preprocess new images
            processed_images = [self.preprocessing_pipeline.process(img) for img in new_images]
            
            # Extract features
            features_list = []
            for extractor in self.feature_extractors:
                extractor_features = [extractor.extract(img) for img in processed_images]
                features_list.append(np.array(extractor_features))
            
            # Combine features
            new_features = np.hstack(features_list)
            
            # Update classifier
            self.classifier.fit(
                np.vstack([self.classifier.features, new_features]),
                list(self.classifier.label_encoder.inverse_transform(self.classifier.labels)) + new_labels
            )
        else:
            # For other classifiers, we need to retrain
            # This is a simplified approach - in practice, you might want to implement
            # more sophisticated online learning methods
            self.fit(new_images, new_labels)


def create_default_pipeline() -> PradaClassificationPipeline:
    """Create a default pipeline with recommended components."""
    # Preprocessors
    preprocessors = [
        ResizePreprocessor(target_size=(224, 224)),
        BackgroundRemovalPreprocessor(),
        NormalizePreprocessor()
    ]
    
    # Feature extractors
    resnet_extractor = ResNetFeatureExtractor(model_name="resnet50")
    pca_extractor = PCAFeatureExtractor(resnet_extractor, n_components=100)
    
    feature_extractors = [pca_extractor]
    
    # Classifiers
    nn_classifier = NearestNeighborClassifier(n_neighbors=5)
    cluster_classifier = ClusteringClassifier(n_clusters=10)
    
    # Ensemble classifier
    ensemble = EnsembleClassifier(
        classifiers=[nn_classifier, cluster_classifier],
        weights=[0.7, 0.3]  # Give more weight to nearest neighbor
    )
    
    # Create pipeline
    pipeline = PradaClassificationPipeline(
        preprocessors=preprocessors,
        feature_extractors=feature_extractors,
        classifier=ensemble
    )
    
    return pipeline 