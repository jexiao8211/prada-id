from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Prada ID"
    
    # # Security
    # SECRET_KEY: str
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    POSTGRES_SERVER: str = "localhost:5433"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "testpass123"
    POSTGRES_DB: str = "Images"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    
    # # Redis
    # REDIS_HOST: str = "localhost"
    # REDIS_PORT: int = 5433
    
    # # AWS
    # AWS_ACCESS_KEY_ID: Optional[str] = None
    # AWS_SECRET_ACCESS_KEY: Optional[str] = None
    # AWS_REGION: str = "us-east-1"
    # S3_BUCKET: Optional[str] = None
    
    # # ML Model
    # MODEL_PATH: str = "models/prada_classifier.pt"
    
    # class Config:
    #     case_sensitive = True
    #     env_file = ".env"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
            )


settings = Settings() 