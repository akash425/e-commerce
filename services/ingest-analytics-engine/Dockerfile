FROM python:3.11-slim

WORKDIR /app

# Copy requirements from project root
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY services/ingest-analytics-engine/ .

# Run the ingestion script
CMD ["python", "main.py"]

