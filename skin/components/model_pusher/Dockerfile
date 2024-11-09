FROM python:3.8.20-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && curl https://sdk.cloud.google.com | bash

ENV PATH="/root/google-cloud-sdk/bin:${PATH}"

# Copy the entire skin directory first
COPY skin /app/skin

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/skin/components/model_pusher/requirements.txt

# Set Python path
ENV PYTHONPATH="/app"

# Command to run the script
CMD ["python", "/app/skin/components/model_pusher/model_pusher.py"]