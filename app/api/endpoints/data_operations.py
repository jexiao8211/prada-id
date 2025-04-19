import time
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
import re
import os

from app.api.deps import get_db
import app.db.models as models


router = APIRouter()


@router.post("/upload_item/")
async def upload_item(image: UploadFile = File(...), season: str = Form(...), db: Session = Depends(get_db)):
    season_dir = os.path.join('C:/Users/jexia/projects/prada-id/app/images', season.replace(' ', '_'))
    os.makedirs(season_dir, exist_ok=True)

    base_image_filename = f"{int(time.time())}.jpg"
    image_path = os.path.join(season_dir, base_image_filename).replace("\\","/")

    # Check if the image path already exists and add a "_<num>" if it does
    if os.path.exists(image_path):
        num = 1
        while os.path.exists(image_path):
            image_filename = f"{base_image_filename.split('.')[0]}_{num}.jpg"
            image_path = os.path.join(season_dir, image_filename).replace("\\","/")
            num += 1

    # Save the uploaded image file
    with open(image_path, "wb") as image_file:
        image_file.write(await image.read())  # Read the image data from the UploadFile

    db_item = models.Images(image_path=image_path, season=season)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item