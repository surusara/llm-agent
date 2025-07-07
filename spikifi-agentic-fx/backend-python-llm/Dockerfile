# Use a lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the source code
COPY . .

# Expose FastAPI port (change to 8500 for ML service)
EXPOSE 8000

# Run FastAPI app (api.py must contain FastAPI app named `app`)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
