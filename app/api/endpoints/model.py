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

@router.post("/switch_models/", response_model=Dict)
async def switch_model(model_name: str = Form(...)):
    # Hard code a model dictionary
    # I want to keep track of the path to the weights, as well as the types of preprocessing and 
    # feature extraction that I need to use for prediction
    pass
    # TODO

@router.post("/classify/", response_model=Dict)
async def classify_image(image: UploadFile = File(...)):
    """
    Classify a Prada clothing image and return the predicted season.
    """
    try:
        # Read and validate the image
        contents = await image.read()
        image = Image.open(io.BytesIO(contents))
        
        # Make prediction
        result = pipeline.predict(image)
        # print(result)

        return result
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing image: {str(e)}"
        )

@router.post("/train/", response_model=Dict)
async def train_model():
    pass
    # TODO

# @router.get("/status")
# async def get_model_status():
#     """
#     Get information about the current model.
#     """
#     return {
#         "is_fitted": pipeline.is_fitted,
#         "preprocessors": [p.__class__.__name__ for p in pipeline.preprocessing_pipeline.preprocessors],
#         "feature_extractors": [e.__class__.__name__ for e in pipeline.feature_extractors],
#         "classifier": pipeline.classifier.__class__.__name__
#     } 