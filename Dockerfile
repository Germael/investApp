# Use the official Python base image
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# Install system dependencies and poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install the latest version of Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set the working directory inside the container
WORKDIR /app

# Copy poetry dependencies configuration and install dependencies
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root --no-dev  # Install only production dependencies

# Copy the src directory and other necessary files
COPY src /app/src

RUN mkdir db

# Expose port for the FastAPI application
EXPOSE 8003

# Start the FastAPI application using uvicorn
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8003"]
