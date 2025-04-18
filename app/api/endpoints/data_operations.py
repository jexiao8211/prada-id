from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, validator
import re
import os

from app.api.deps import get_db
import app.db.models as models


router = APIRouter()

# Define Pydantic models
class Item(BaseModel):
    img_path: str
    season: str

    @validator('img_path')
    def validate_img_path(cls, value):
        # Check if the path exists
        if not os.path.exists(value):
            raise ValueError(f"The path '{value}' does not exist.")
        return value

    @validator('season')
    def validate_season(cls, value):
        if not re.compile(r'^(Spring Summer|Fall Winter) \d{4}$').match(value):
            raise ValueError("Season must start with 'Spring Summer' or 'Fall Winter' and end with a 4-digit year.")
        return value    


@router.post("/item/")
async def create_item(item: Item, db: Session = Depends(get_db)):
    db_item = models.Images(image_path=item.img_path, season=item.season)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
