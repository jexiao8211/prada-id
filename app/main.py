from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import classify, training
from app.core.config import settings

app = FastAPI(
    title="Prada ID",
    description="API for classifying vintage Prada clothing by season",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(classify.router, prefix=settings.API_V1_STR + "/classify", tags=["classification"])
app.include_router(training.router, prefix=settings.API_V1_STR + "/training", tags=["training"])

@app.get("/")
async def root():
    return {"message": "Welcome to Prada ID API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 