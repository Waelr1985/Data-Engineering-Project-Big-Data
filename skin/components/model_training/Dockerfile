FROM python:3.8-slim

# Set environment variables
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

# Copy and install requirements
# Changed path to model_training requirements
COPY skin/components/model_training/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pyspark==3.3.2

# Copy application files - fixed file names and paths
COPY skin/components/model_training/config.py /app/
COPY skin/components/model_training/model_training.py /app/

# Create artifacts directory structure
RUN mkdir -p artifacts/model artifacts/transformed_data/train artifacts/transformed_data/test

# Create non-root user
RUN useradd -m -s /bin/bash appuser && \
    chown -R appuser:appuser /app /opt/spark

USER appuser

# Mount artifacts directory
VOLUME ["/app/artifacts"]

CMD ["python", "model_training.py"]