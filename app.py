from fastapi import FastAPI, HTTPException, BackgroundTasks, File, UploadFile
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import uvicorn
import logging
from datetime import datetime
import os
import shutil
import json

# Import all services
from data_ingestion import DataIngestion
from data_validation import DataValidation, CustomException
from data_transformation import DataTransformationService
from model_training import ModelTrainer
from model_evaluation import ModelEvaluator
from model_pusher import ModelPusher
from model_predictor import ModelPredictor

app = FastAPI(title="Skin Disease Classification API")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Pydantic models for requests/responses
class PredictionInput(BaseModel):
    B: int = Field(..., ge=0, le=255)
    G: int = Field(..., ge=0, le=255)
    R: int = Field(..., ge=0, le=255)

class PredictionResponse(BaseModel):
    prediction: int
    prediction_label: str
    confidence: float
    input_features: Dict[str, int]

class TrainingResponse(BaseModel):
    status: str
    model_path: str
    metrics: Dict[str, float]
    timestamp: str

class EvaluationResponse(BaseModel):
    status: str
    metrics: Dict[str, float]
    timestamp: str

# Pipeline Status Endpoint
@app.get("/pipeline-status")
async def get_pipeline_status():
    try:
        return {
            "ingestion_complete": os.path.exists("artifacts/raw_data"),
            "validation_complete": os.path.exists("artifacts/validated_data"),
            "transformation_complete": os.path.exists("artifacts/transformed_data"),
            "model_trained": os.path.exists("artifacts/models"),
            "model_evaluated": os.path.exists("artifacts/metrics"),
            "model_pushed": os.path.exists("artifacts/production_model"),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Full Pipeline Endpoint
@app.post("/run-pipeline")
async def run_full_pipeline(background_tasks: BackgroundTasks):
    try:
        # Initialize all services
        ingestion_service = DataIngestion()
        validation_service = DataValidation()
        transformation_service = DataTransformationService()
        training_service = ModelTrainer()
        evaluation_service = ModelEvaluator()
        pusher_service = ModelPusher()

        # Run pipeline steps
        background_tasks.add_task(ingestion_service.upload_zip_to_gcloud_from_url)
        background_tasks.add_task(validation_service.validate)
        background_tasks.add_task(transformation_service.transform_and_save)
        background_tasks.add_task(training_service.train_model)
        background_tasks.add_task(evaluation_service.evaluate_model)
        background_tasks.add_task(pusher_service.push_model)

        return {
            "status": "Pipeline started successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Model Training Endpoint
@app.post("/train-model", response_model=TrainingResponse)
async def train_model():
    try:
        trainer = ModelTrainer()
        model_path = trainer.train_model()
        
        return TrainingResponse(
            status="Model training completed",
            model_path=model_path,
            metrics=trainer.get_metrics(),
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Model Evaluation Endpoint
@app.post("/evaluate-model", response_model=EvaluationResponse)
async def evaluate_model():
    try:
        evaluator = ModelEvaluator()
        metrics = evaluator.evaluate_model()
        
        return EvaluationResponse(
            status="Model evaluation completed",
            metrics=metrics,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Model Push Endpoint
@app.post("/push-model")
async def push_model():
    try:
        pusher = ModelPusher()
        result = pusher.push_model()
        
        return {
            "status": "Model pushed successfully",
            "destination": result["destination"],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Prediction Endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(input_data: PredictionInput):
    try:
        predictor = ModelPredictor()
        result = predictor.predict({
            "B": input_data.B,
            "G": input_data.G,
            "R": input_data.R
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Batch Prediction Endpoint
@app.post("/predict-batch")
async def predict_batch(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        predictor = ModelPredictor()
        results = predictor.predict_batch(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        return {
            "predictions": results,
            "count": len(results),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Model Metrics Endpoint
@app.get("/model-metrics")
async def get_model_metrics():
    try:
        evaluator = ModelEvaluator()
        return evaluator.get_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)