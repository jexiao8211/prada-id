from typing import Dict, List, Optional

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Form
from PIL import Image
import io
import numpy as np

from app.ml.pipeline import PradaClassificationPipeline, create_default_pipeline
from app.core.config import settings

router = APIRouter()

# Initialize the pipeline
pipeline = create_default_pipeline()


@router.post("/classify", response_model=Dict)
async def classify_image(file: UploadFile = File(...)):
    """
    Classify a Prada clothing image and return the predicted season.
    """
    try:
        # Read and validate the image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Make prediction
        result = pipeline.predict(image)
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing image: {str(e)}"
        )


@router.post("/contribute")
async def contribute_image(
    file: UploadFile = File(...),
    season: str = Form(...),
    confidence: Optional[float] = Form(None)
):
    """
    Contribute a labeled image to improve the model.
    """
    try:
        # Read and validate the image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Update the model with the new data
        pipeline.update([image], [season])
        
        return {"status": "success", "message": "Image contributed successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error contributing image: {str(e)}"
        )


@router.get("/model/status")
async def get_model_status():
    """
    Get information about the current model.
    """
    return {
        "is_fitted": pipeline.is_fitted,
        "preprocessors": [p.__class__.__name__ for p in pipeline.preprocessing_pipeline.preprocessors],
        "feature_extractors": [e.__class__.__name__ for e in pipeline.feature_extractors],
        "classifier": pipeline.classifier.__class__.__name__
    } 