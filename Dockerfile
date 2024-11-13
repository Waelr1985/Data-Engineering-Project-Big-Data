# Base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create organized artifact structure
RUN mkdir -p artifacts && \
    mkdir -p artifacts/data_ingestion/raw_data \
             artifacts/data_ingestion/extracted_data \
             artifacts/data_validation/drift_report \
             artifacts/data_transformation/transformed_data \
             artifacts/model_trainer/model \
             artifacts/model_evaluation/evaluation \
             artifacts/model_pusher/production_model

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    CONFIG_PATH=/app/config.yaml

# Copy the application code
COPY . .

# Create non-root user for security
RUN useradd -m -s /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8080

# Add health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]