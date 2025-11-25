#
FROM python:3.14-slim

# Install curl
RUN apt-get update && apt-get install -y curl

# create /app directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy python requirements
COPY pyproject.toml .

# Install dependencies
RUN uv pip install --system -r pyproject.toml

# Copy application code
COPY . .

# Expose the port
EXPOSE 4000

# Command to run the application with auto-reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "4000", "--reload"]