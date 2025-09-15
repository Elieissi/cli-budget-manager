FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir jsonschema

# Run CLI app when container starts
CMD ["python", "main.py"]
