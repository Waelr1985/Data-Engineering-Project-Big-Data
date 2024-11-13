FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"
ENV PYTHONPATH=/app
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin

# Install Java and other dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-17-jre-headless \
        openjdk-17-jdk-headless \
        gcc \
        python3-dev \
        procps \
        wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download and install Spark
RUN wget https://archive.apache.org/dist/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz && \
    tar -xzf spark-3.3.2-bin-hadoop3.tgz && \
    mv spark-3.3.2-bin-hadoop3 /opt/spark && \
    rm spark-3.3.2-bin-hadoop3.tgz

WORKDIR /app

# Copy requirements file and install dependencies
COPY skin/components/model_predictor/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create directories with proper permissions
RUN mkdir -p /app/artifacts/imported_model && \
    chmod -R 777 /app/artifacts

# Copy the application files
COPY skin/components/model_predictor/model_predictor.py /app/
COPY skin/configuration/gcloud.py /app/

# Create a non-root user and set permissions
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app && \
    chmod -R 777 /app/artifacts
USER appuser

# Add directory check on startup
CMD ["python", "model_predictor.py"]