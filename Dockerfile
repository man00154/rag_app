# Use official Python slim image with Python 3.11
FROM python:3.11-slim

# Install system dependencies needed by FAISS and build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    libomp-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory in container
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Upgrade pip and install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy your app code to container
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Run your app with Streamlit on all interfaces
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
