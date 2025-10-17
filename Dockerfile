FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and necessary files
COPY app.py .
COPY src/ ./src/
COPY params.yaml .
COPY models/ ./models/
COPY data/processed/ ./data/processed/

# Copy frontend files
COPY templates/ ./templates/
COPY static/ ./static/

# Expose port
EXPOSE 8080

# Run the Flask application
CMD ["python", "app.py"]
