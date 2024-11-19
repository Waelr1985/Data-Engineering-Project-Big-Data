FROM python:3.8-slim

# Install tk and dependencies
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the data validation service requirements first
COPY skin/components/data_validation/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy only the necessary application code
COPY . .
COPY skin/components/data_validation /app/data_validation

# Create validation report directory
RUN mkdir -p artifacts/data_validation/drift_report

# Set Python path
ENV PYTHONPATH=/app

# Run the validation script
CMD ["python", "data_validation/data_validation.py"]