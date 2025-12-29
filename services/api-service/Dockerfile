FROM python:3.11-slim

WORKDIR /app

# Copy requirements from project root
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY services/api-service/ .

# Copy ingest-analytics-engine for imports
COPY services/ingest-analytics-engine/ ./ingest-analytics-engine/

# Expose port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]

