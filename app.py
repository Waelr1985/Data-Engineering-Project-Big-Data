from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import logging
import uvicorn
from datetime import datetime

# Import skin package components
from skin.components.model_predictor.model_predictor import ModelPredictor
from skin.components.data_ingestion.data_ingestion import DataIngestion
from skin.components.data_validation.data_validation import DataValidation
from skin.components.data_validation.config import DataValidationConfig
from skin.components.data_transformation.data_transformation import DataTransformation
from skin.components.model_training.model_training import ModelTrainer
from skin.components.model_evaluation.model_evaluation import ModelEvaluator
from skin.components.model_pusher.model_pusher import ModelPusher
from skin.configuration.gcloud import GCloud

# Set up configuration
config = DataValidationConfig()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Skin Detection API",
    description="API for skin detection using RGB values",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
try:
    gcloud = GCloud()
    
    data_ingestion = DataIngestion()
    data_validation = DataValidation(config=config)
    data_transformation = DataTransformation()
    training_pipeline = ModelTrainer()
    model_evaluation = ModelEvaluator()
    model_pusher = ModelPusher()
    model_predictor = ModelPredictor()
    logger.info("All components initialized successfully")
except Exception as e:
    logger.error(f"Error initializing components: {str(e)}")
    raise

# Pydantic models
class RGBInput(BaseModel):
    r: int = Field(..., ge=0, le=255, description="Red value (0-255)")
    g: int = Field(..., ge=0, le=255, description="Green value (0-255)")
    b: int = Field(..., ge=0, le=255, description="Blue value (0-255)")

class PipelineStatus(BaseModel):
    is_running: bool
    stage: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    error: Optional[str] = None

# API endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Skin Detection API",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/ingest-data")
async def ingest_data(background_tasks: BackgroundTasks):
    """Start data ingestion process"""
    try:
        background_tasks.add_task(data_ingestion.initiate_data_ingestion)
        return {"message": "Data ingestion started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate-data")
async def validate_data(background_tasks: BackgroundTasks):
    """Start data validation process"""
    try:
        background_tasks.add_task(data_validation.initiate_data_validation)
        return {"message": "Data validation started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transform-data")
async def transform_data(background_tasks: BackgroundTasks):
    """Start data transformation process"""
    try:
        background_tasks.add_task(data_transformation.initiate_data_transformation)
        return {"message": "Data transformation started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train-model")
async def train_model(background_tasks: BackgroundTasks):
    """Start model training process"""
    try:
        background_tasks.add_task(training_pipeline.initiate_model_training)
        return {"message": "Model training started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/evaluate-model")
async def evaluate_model(background_tasks: BackgroundTasks):
    """Start model evaluation process"""
    try:
        background_tasks.add_task(model_evaluation.run_evaluation)
        return {"message": "Model evaluation started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/push-model")
async def push_model(background_tasks: BackgroundTasks):
    """Start model pushing process"""
    try:
        background_tasks.add_task(model_pusher.push_model_to_gcp)
        return {"message": "Model pushing started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
async def predict_skin(rgb_input: RGBInput):
    """
    Predict skin classification from RGB values
    Returns prediction (0/1), label (Skin/Non-Skin), and confidence score
    """
    try:
        result = model_predictor.predict(
            r=rgb_input.r,
            g=rgb_input.g,
            b=rgb_input.b
        )
        
        return {
            "status": "success",
            "prediction": result["prediction"],
            "prediction_label": result["prediction_label"],
            "confidence": result["confidence"],
            "input_values": {
                "r": rgb_input.r,
                "g": rgb_input.g,
                "b": rgb_input.b
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)