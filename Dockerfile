FROM python:3.8-slim

# Install system dependencies including Java
RUN apt-get update && \
    apt-get install -y \
    default-jdk \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    tk-dev \
    python3-tk && \
    rm -rf /var/lib/apt/lists/*

# Set Java environment variables correctly
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Set Spark environment variables
ENV SPARK_HOME=/usr/local/lib/python3.8/site-packages/pyspark
ENV PATH="${SPARK_HOME}/bin:${PATH}"

WORKDIR /app

# Copy requirements first
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy setup.py and package
COPY setup.py .
COPY skin/ ./skin/
RUN pip install -e .

# Copy the rest of the application
COPY . .

# Verify Java installation
RUN java -version

EXPOSE 8000
CMD ["/usr/local/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]