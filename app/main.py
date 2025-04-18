from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Annotated

# from app.api.endpoints import classify, training, data_operations
from app.api.endpoints import data_operations

from app.core.config import settings
from app.db.session import engine
import app.db.models as models


app = FastAPI(
    title="Prada ID",
    description="API for classifying vintage Prada clothing by season",
    version="0.1.0",
)
models.Base.metadata.create_all(bind=engine)    # create all the tables in the database


# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  # React frontend
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Include routers
# app.include_router(classify.router, prefix=settings.API_V1_STR + "/classify", tags=["classification"])
# app.include_router(training.router, prefix=settings.API_V1_STR + "/training", tags=["training"])
app.include_router(data_operations.router, prefix=settings.API_V1_STR + "/data_operations", tags=["data_operations"])

@app.get("/")
async def root():
    return {"message": "Welcome to Prada ID API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 