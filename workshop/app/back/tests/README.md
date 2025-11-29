# Backend Testing Documentation

This directory contains the test suite for the Backend service.

## Structure

- **`conftest.py`**: Pytest configuration and fixtures. Sets up the `TestClient` and the in-memory SQLite database for isolation.
- **`app/test_main.py`**: Tests for the main application entry point and health checks.
- **`app/routes/`**: Tests specific to each API router (Users, AI, SWAPI).

## Running Tests

Tests are designed to run inside the Docker container to ensure the environment matches production.

### Command

From the project root:

```bash
docker compose exec back pytest
```

### Options

- **Verbose output**:
  ```bash
  docker compose exec back pytest -v
  ```
- **Stop on first failure**:
  ```bash
  docker compose exec back pytest -x
  ```
- **Run specific test file**:
  ```bash
  docker compose exec back pytest tests/app/routes/test_users.py
  ```
