import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

import numpy as np
from PIL import Image
import io
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import ModelVersion
from app.ml.pipeline import PradaClassificationPipeline, create_default_pipeline
from app.services.data_service import DataService


logger = logging.getLogger(__name__)


class TrainingService:
    """Service for managing model training."""
    
    def __init__(self, db: Session, data_service: DataService):
        self.db = db
        self.data_service = data_service
        self.pipeline = None
        self.models_dir = "models"
        
        # Create models directory if it doesn't exist
        os.makedirs(self.models_dir, exist_ok=True)
    
    def train_model(self, verified_only: bool = True) -> Dict[str, Any]:
        """Train the model on the available data."""
        try:
            # Get training data
            image_urls, labels = self.data_service.get_training_data(verified_only=verified_only)
            
            if not image_urls:
                return {"status": "error", "message": "No training data available"}
            
            # Download and process images
            images = []
            for url in image_urls:
                try:
                    image_data = self.data_service.download_image(url)
                    image = Image.open(io.BytesIO(image_data))
                    images.append(image)
                except Exception as e:
                    logger.warning(f"Failed to process image {url}: {str(e)}")
            
            if not images:
                return {"status": "error", "message": "Failed to process any images"}
            
            # Create and train pipeline
            self.pipeline = create_default_pipeline()
            self.pipeline.fit(images, labels)
            
            # Save model
            version = datetime.now().strftime("%Y%m%d%H%M%S")
            model_path = os.path.join(self.models_dir, f"prada_classifier_{version}.pt")
            
            # For now, we'll just save a placeholder since our pipeline doesn't have a direct save method
            # In a real implementation, you would save the model state
            with open(model_path, 'w') as f:
                json.dump({"version": version, "timestamp": datetime.now().isoformat()}, f)
            
            # Save model version to database
            model_version = ModelVersion(
                version=version,
                path=model_path,
                metrics=json.dumps({"num_samples": len(images)}),
                is_active=1
            )
            
            # Deactivate previous models
            self.db.query(ModelVersion).filter(ModelVersion.is_active == 1).update({"is_active": 0})
            
            # Add new model version
            self.db.add(model_version)
            self.db.commit()
            
            return {
                "status": "success",
                "message": "Model trained successfully",
                "version": version,
                "num_samples": len(images)
            }
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            return {"status": "error", "message": f"Error training model: {str(e)}"}
    
    def get_model(self, version: Optional[str] = None) -> PradaClassificationPipeline:
        """Get a trained model, either the latest or a specific version."""
        if self.pipeline is not None and self.pipeline.is_fitted:
            return self.pipeline
        
        # If no version specified, get the active model
        if version is None:
            model_version = self.db.query(ModelVersion).filter(ModelVersion.is_active == 1).first()
        else:
            model_version = self.db.query(ModelVersion).filter(ModelVersion.version == version).first()
        
        if model_version is None:
            # If no model found, create a new one
            self.pipeline = create_default_pipeline()
            return self.pipeline
        
        # Load the model
        # In a real implementation, you would load the model state
        # For now, we'll just create a new pipeline
        self.pipeline = create_default_pipeline()
        
        # Train the model on the available data
        image_urls, labels = self.data_service.get_training_data(verified_only=True)
        
        if image_urls:
            images = []
            for url in image_urls:
                try:
                    image_data = self.data_service.download_image(url)
                    image = Image.open(io.BytesIO(image_data))
                    images.append(image)
                except Exception as e:
                    logger.warning(f"Failed to process image {url}: {str(e)}")
            
            if images:
                self.pipeline.fit(images, labels)
        
        return self.pipeline
    
    def get_model_versions(self) -> List[Dict[str, Any]]:
        """Get all model versions."""
        versions = self.db.query(ModelVersion).all()
        return [
            {
                "version": v.version,
                "path": v.path,
                "metrics": json.loads(v.metrics) if v.metrics else {},
                "is_active": v.is_active,
                "created_at": v.created_at.isoformat()
            }
            for v in versions
        ] 