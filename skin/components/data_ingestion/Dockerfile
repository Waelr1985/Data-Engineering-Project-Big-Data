FROM python:3.10-slim

WORKDIR /app

# Copy only the requirements first to leverage Docker cache
COPY skin/components/data_ingestion/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
#ENV GOOGLE_APPLICATION_CREDENTIALS=/app/key.json

# Run the data ingestion script
CMD ["python", "-m", "skin.components.data_ingestion.data_ingestion"]
