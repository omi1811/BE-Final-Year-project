# Use official Python image from Docker Hub
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy all project files to container
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set the default command
CMD ["python", "main.py"]
