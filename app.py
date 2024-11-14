from fastapi import FastAPI, HTTPException, BackgroundTasks, File, UploadFile
from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime
import os
import shutil
import logging

# Import services
from components.data_ingestion.data_ingestion import DataIngestion
from components.data_validation.data_validation import DataValidation
from components.data_transformation.data_transformation import DataTransformationService
from components.model_training.model_training import ModelTrainer
from components.model_evaluation.model_evaluation import ModelEvaluator
from components.model_pusher.model_pusher import ModelPusher
from components.model_predictor.model_predictor import ModelPredictor

app = FastAPI(title="Skin Segmentation API")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
    timestamp: str

# Helper function to check if an artifact exists
def check_artifact_exists(path: str) -> bool:
    return os.path.exists(path)

# Pipeline Status Endpoint
@app.get("/pipeline-status")
async def get_pipeline_status():
    try:
        return {
            "ingestion_complete": check_artifact_exists("artifacts/raw_data"),
            "validation_complete": check_artifact_exists("artifacts/validated_data"),
            "transformation_complete": check_artifact_exists("artifacts/transformed_data"),
            "model_trained": check_artifact_exists("artifacts/trained_model"),
            "model_evaluated": check_artifact_exists("artifacts/evaluated_model"),
            "model_pushed": check_artifact_exists("artifacts/production_model"),
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

        # Run pipeline steps in background tasks
        background_tasks.add_task(ingestion_service.upload_zip_to_gcloud_from_url)
        background_tasks.add_task(validation_service.validate)
        background_tasks.add_task(transformation_service.transform_and_save)
        background_tasks.add_task(training_service.run_training_pipeline)
        background_tasks.add_task(evaluation_service.run_evaluation)
        background_tasks.add_task(pusher_service.push_model_to_gcp)

        return {
            "status": "Pipeline started successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Data Ingestion Endpoint
@app.post("/ingest-data")
async def ingest_data():
    try:
        ingestion_service = DataIngestion()
        ingestion_service.upload_zip_to_gcloud_from_url()
        return {"status": "Data ingestion completed", "timestamp": datetime.now().isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Data Validation Endpoint
@app.post("/validate-data")
async def validate_data():
    try:
        if not check_artifact_exists("artifacts/raw_data"):
            raise HTTPException(status_code=400, detail="Data ingestion not completed yet.")
        
        validation_service = DataValidation()
        validation_service.validate()
        return {"status": "Data validation completed", "timestamp": datetime.now().isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Data Transformation Endpoint
@app.post("/transform-data")
async def transform_data():
    try:
        if not check_artifact_exists("artifacts/validated_data"):
            raise HTTPException(status_code=400, detail="Data validation not completed yet.")
        
        transformation_service = DataTransformationService()
        transformation_service.transform_and_save()
        return {"status": "Data transformation completed", "timestamp": datetime.now().isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Model Training Endpoint
@app.post("/train-model", response_model=TrainingResponse)
async def train_model():
    try:
        if not check_artifact_exists("artifacts/transformed_data"):
            raise HTTPException(status_code=400, detail="Data transformation not completed yet.")
        
        trainer = ModelTrainer()
        model_path = trainer.run_training_pipeline()
        
        return TrainingResponse(
            status="Model training completed",
            model_path=model_path,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Model Evaluation Endpoint
@app.post("/evaluate-model")
async def evaluate_model():
    try:
        if not check_artifact_exists("artifacts/trained_model"):
            raise HTTPException(status_code=400, detail="Model training not completed yet.")
        
        evaluator = ModelEvaluator()
        evaluation_metrics = evaluator.evaluate()
        
        return {
            "status": "Model evaluation completed",
            "evaluation_metrics": evaluation_metrics,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Model Pusher Endpoint
@app.post("/push-model")
async def push_model():
    try:
        if not check_artifact_exists("artifacts/evaluated_model"):
            raise HTTPException(status_code=400, detail="Model evaluation not completed yet.")
        
        pusher = ModelPusher()
        model_gcp_path = pusher.push_model_to_gcp()
        
        return {
            "status": "Model pushed to GCP",
            "model_gcp_path": model_gcp_path,
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
        
        return PredictionResponse(
            prediction=result['prediction'],
            prediction_label=result['prediction_label'],
            confidence=result['confidence'],
            input_features=result['input_features']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
