from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder


class Classifier(ABC):
    """Base class for classification models."""
    
    @abstractmethod
    def fit(self, features: np.ndarray, labels: List[str]) -> None:
        """Fit the classifier on training data."""
        pass
    
    @abstractmethod
    def predict(self, features: np.ndarray) -> Dict[str, Any]:
        """Make a prediction on the input features."""
        pass


class NearestNeighborClassifier(Classifier):
    """Classify using nearest neighbor approach."""
    
    def __init__(self, n_neighbors: int = 5, metric: str = "euclidean"):
        self.n_neighbors = n_neighbors
        self.metric = metric
        self.model = NearestNeighbors(n_neighbors=n_neighbors, metric=metric)
        self.label_encoder = LabelEncoder()
        self.features = None
        self.labels = None
        self.is_fitted = False
    
    def fit(self, features: np.ndarray, labels: List[str]) -> None:
        """Fit the nearest neighbor model."""
        self.features = features
        self.labels = self.label_encoder.fit_transform(labels)
        self.model.fit(features)
        self.is_fitted = True
    
    def predict(self, features: np.ndarray) -> Dict[str, Any]:
        """Predict the class of the input features."""
        if not self.is_fitted:
            raise ValueError("Classifier must be fitted before use")
        
        # Find nearest neighbors
        distances, indices = self.model.kneighbors(features.reshape(1, -1))
        
        # Get labels of nearest neighbors
        neighbor_labels = self.labels[indices[0]]
        
        # Count occurrences of each label
        unique_labels, counts = np.unique(neighbor_labels, return_counts=True)
        
        # Find the most common label
        most_common_idx = np.argmax(counts)
        predicted_label = self.label_encoder.inverse_transform([unique_labels[most_common_idx]])[0]
        
        # Calculate confidence as the proportion of the most common label
        confidence = counts[most_common_idx] / self.n_neighbors
        
        # Calculate probabilities for each class
        probabilities = {}
        for i, label in enumerate(self.label_encoder.classes_):
            count = np.sum(neighbor_labels == self.label_encoder.transform([label])[0])
            probabilities[label] = count / self.n_neighbors
        
        return {
            "season": predicted_label,
            "confidence": confidence,
            "probabilities": probabilities,
            "nearest_neighbors": {
                "distances": distances[0].tolist(),
                "indices": indices[0].tolist()
            }
        }


class ClusteringClassifier(Classifier):
    """Classify using clustering approach."""
    
    def __init__(self, n_clusters: int = 10, random_state: int = 42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.model = KMeans(n_clusters=n_clusters, random_state=random_state)
        self.cluster_labels = {}  # Maps cluster IDs to season labels
        self.is_fitted = False
    
    def fit(self, features: np.ndarray, labels: List[str]) -> None:
        """Fit the clustering model."""
        # Fit the clustering model
        self.model.fit(features)
        
        # Assign labels to clusters based on majority vote
        for i in range(self.n_clusters):
            cluster_indices = np.where(self.model.labels_ == i)[0]
            if len(cluster_indices) > 0:
                cluster_labels = [labels[j] for j in cluster_indices]
                unique_labels, counts = np.unique(cluster_labels, return_counts=True)
                most_common_idx = np.argmax(counts)
                self.cluster_labels[i] = unique_labels[most_common_idx]
        
        self.is_fitted = True
    
    def predict(self, features: np.ndarray) -> Dict[str, Any]:
        """Predict the class of the input features."""
        if not self.is_fitted:
            raise ValueError("Classifier must be fitted before use")
        
        # Predict cluster
        cluster = self.model.predict(features.reshape(1, -1))[0]
        
        # Get label for the cluster
        predicted_label = self.cluster_labels.get(cluster, "Unknown")
        
        # Calculate distance to cluster center
        distance = np.linalg.norm(features - self.model.cluster_centers_[cluster])
        
        # Calculate confidence based on distance (inverse relationship)
        max_distance = np.max([np.linalg.norm(features - center) for center in self.model.cluster_centers_])
        confidence = 1 - (distance / max_distance)
        
        # Calculate probabilities for each cluster
        probabilities = {}
        for i in range(self.n_clusters):
            dist = np.linalg.norm(features - self.model.cluster_centers_[i])
            prob = 1 - (dist / max_distance)
            label = self.cluster_labels.get(i, "Unknown")
            probabilities[label] = prob
        
        # Normalize probabilities
        total = sum(probabilities.values())
        if total > 0:
            probabilities = {k: v/total for k, v in probabilities.items()}
        
        return {
            "season": predicted_label,
            "confidence": confidence,
            "probabilities": probabilities,
            "cluster": int(cluster)
        }


class EnsembleClassifier(Classifier):
    """Combine multiple classifiers for better performance."""
    
    def __init__(self, classifiers: List[Classifier], weights: Optional[List[float]] = None):
        self.classifiers = classifiers
        self.weights = weights if weights else [1.0] * len(classifiers)
        self.is_fitted = False
    
    def fit(self, features: np.ndarray, labels: List[str]) -> None:
        """Fit all classifiers."""
        for classifier in self.classifiers:
            classifier.fit(features, labels)
        self.is_fitted = True
    
    def predict(self, features: np.ndarray) -> Dict[str, Any]:
        """Combine predictions from all classifiers."""
        if not self.is_fitted:
            raise ValueError("Ensemble classifier must be fitted before use")
        
        # Get predictions from all classifiers
        predictions = [classifier.predict(features) for classifier in self.classifiers]
        
        # Combine predictions based on weights
        combined_probabilities = {}
        for i, pred in enumerate(predictions):
            weight = self.weights[i]
            for label, prob in pred["probabilities"].items():
                if label in combined_probabilities:
                    combined_probabilities[label] += prob * weight
                else:
                    combined_probabilities[label] = prob * weight
        
        # Normalize probabilities
        total = sum(combined_probabilities.values())
        if total > 0:
            combined_probabilities = {k: v/total for k, v in combined_probabilities.items()}
        
        # Find the label with highest probability
        predicted_label = max(combined_probabilities.items(), key=lambda x: x[1])[0]
        confidence = combined_probabilities[predicted_label]
        
        return {
            "season": predicted_label,
            "confidence": confidence,
            "probabilities": combined_probabilities,
            "individual_predictions": predictions
        } 