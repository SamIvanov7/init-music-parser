# Use the official Python base image
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files and to ensure output is flushed
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install build dependencies and ffmpeg
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    libssl-dev \
    build-essential \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt to the working directory
COPY requirements.txt /app/

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Optionally, remove build dependencies to reduce image size
# Uncomment the following lines if you want to remove build tools after installation
# RUN apt-get purge -y --auto-remove gcc build-essential libffi-dev libssl-dev \
#     && rm -rf /var/lib/apt/lists/*

COPY . /app/

CMD ["python", "main.py"]
