from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.data_service import DataService
from app.services.training_service import TrainingService

router = APIRouter()


def get_data_service(db: Session = Depends(get_db)) -> DataService:
    return DataService(db)


def get_training_service(
    db: Session = Depends(get_db),
    data_service: DataService = Depends(get_data_service)
) -> TrainingService:
    return TrainingService(db, data_service)


@router.post("/train")
async def train_model(
    verified_only: bool = Query(True, description="Only use verified contributions for training"),
    training_service: TrainingService = Depends(get_training_service)
) -> Dict:
    """
    Train the model on the available data.
    """
    result = training_service.train_model(verified_only=verified_only)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@router.get("/models")
async def get_model_versions(
    training_service: TrainingService = Depends(get_training_service)
) -> List[Dict]:
    """
    Get all model versions.
    """
    return training_service.get_model_versions()


@router.get("/data/stats")
async def get_data_stats(
    data_service: DataService = Depends(get_data_service)
) -> Dict:
    """
    Get statistics about the training data.
    """
    return data_service.get_contribution_stats()


@router.get("/data/seasons")
async def get_seasons(
    data_service: DataService = Depends(get_data_service)
) -> List[str]:
    """
    Get all unique seasons in the dataset.
    """
    return data_service.get_all_seasons() 