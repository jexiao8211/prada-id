import os
import json
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

import boto3
from botocore.exceptions import ClientError
from sqlalchemy.orm import Session
from fastapi import UploadFile

from app.core.config import settings
from app.db.models import ImageContribution, User
from app.ml.pipeline import PradaClassificationPipeline


class DataService:
    """Service for managing image data and model training data."""
    
    def __init__(self, db: Session, s3_client=None):
        self.db = db
        self.s3_client = s3_client or boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.S3_BUCKET
    
    async def upload_image(self, file: UploadFile, user_id: int) -> str:
        """Upload an image to S3 and return the URL."""
        try:
            # Generate a unique filename
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"images/{user_id}/{timestamp}_{file.filename}"
            
            # Upload to S3
            self.s3_client.upload_fileobj(
                file.file,
                self.bucket_name,
                filename,
                ExtraArgs={'ContentType': file.content_type}
            )
            
            # Generate URL
            url = f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"
            return url
        except ClientError as e:
            raise Exception(f"Failed to upload image: {str(e)}")
    
    def save_contribution(self, user_id: int, image_url: str, season: str, confidence: Optional[float] = None) -> ImageContribution:
        """Save an image contribution to the database."""
        contribution = ImageContribution(
            user_id=user_id,
            image_url=image_url,
            season=season,
            confidence=confidence
        )
        self.db.add(contribution)
        self.db.commit()
        self.db.refresh(contribution)
        return contribution
    
    def get_training_data(self, verified_only: bool = True) -> Tuple[List[str], List[str]]:
        """Get training data for model training."""
        query = self.db.query(ImageContribution)
        if verified_only:
            query = query.filter(ImageContribution.is_verified == 1)
        
        contributions = query.all()
        
        # Extract image URLs and labels
        image_urls = [c.image_url for c in contributions]
        labels = [c.season for c in contributions]
        
        return image_urls, labels
    
    def download_image(self, image_url: str) -> bytes:
        """Download an image from S3."""
        try:
            # Extract key from URL
            key = image_url.split(f"{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/")[1]
            
            # Download from S3
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=key
            )
            
            return response['Body'].read()
        except ClientError as e:
            raise Exception(f"Failed to download image: {str(e)}")
    
    def get_all_seasons(self) -> List[str]:
        """Get all unique seasons from the database."""
        seasons = self.db.query(ImageContribution.season).distinct().all()
        return [season[0] for season in seasons]
    
    def get_contribution_stats(self) -> Dict[str, Any]:
        """Get statistics about contributions."""
        total = self.db.query(ImageContribution).count()
        verified = self.db.query(ImageContribution).filter(ImageContribution.is_verified == 1).count()
        seasons = self.get_all_seasons()
        
        return {
            "total_contributions": total,
            "verified_contributions": verified,
            "unique_seasons": len(seasons),
            "seasons": seasons
        } 