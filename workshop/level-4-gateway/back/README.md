# Backend Service

This directory contains the backend service for the Jedy-StarWarsKubernetes project. It is a Python-based RESTful API built with the [FastAPI](https://fastapi.tiangolo.com/) framework.

## Architecture

The backend service is responsible for:

- **User Management**: Handling user registration and login.
- **SWAPI Proxy**: Acting as a backend-for-frontend (BFF) by fetching data from the public [Star Wars API (SWAPI)](https://swapi.dev/).
- **Database Interaction**: Using [SQLModel](https://sqlmodel.tiangolo.com/) to interact with the PostgreSQL database for storing user data.

## API Documentation

FastAPI automatically generates interactive API documentation conforming to the **OpenAPI** standard.

### Interactive Docs (Swagger UI)
Explore and test the API endpoints directly from your browser.

- **Local Development**: [http://localhost:4000/docs](http://localhost:4000/docs)
- **Kubernetes / Ingress**: [http://localhost/api/docs](http://localhost/api/docs)

### Alternative Docs (ReDoc)
A clean and structured API reference view.

- **Local Development**: [http://localhost:4000/redoc](http://localhost:4000/redoc)
- **Kubernetes / Ingress**: [http://localhost/api/redoc](http://localhost/api/redoc)

### OpenAPI JSON Schema
The raw OpenAPI definition file is available at:
- **Local**: `http://localhost:4000/openapi.json`
- **Kubernetes**: `http://localhost/api/openapi.json`

## Dependencies

The main dependencies for this service are:

- `fastapi`: The web framework.
- `uvicorn`: The ASGI server.
- `sqlmodel`: The database ORM.
- `psycopg2-binary`: The PostgreSQL adapter for Python.
- `python-jose[cryptography]`: For JWT creation and validation.
- `passlib[bcrypt]`: For password hashing.
- `httpx`: For making HTTP requests to the SWAPI.
- `pytest`: The testing framework.

For a complete list of dependencies, please see the `pyproject.toml` file.

### Dependency Management with `uv`

This project uses [uv](https://github.com/astral-sh/uv), an extremely fast Python package installer and resolver, written in Rust. It serves as a drop-in replacement for `pip` and `pip-tools` in our Docker builds to significantly reduce build times.

In the `Dockerfile`, you will see:
```dockerfile
# Installing dependencies with uv
RUN uv pip install --system -r pyproject.toml
```

If you are developing locally without Docker, you can install `uv` and use it to manage your virtual environment:

```bash
pip install uv
uv venv
source .venv/bin/activate
uv pip install -r pyproject.toml
```

## Docker Management

### Build without Cache
If you need to force a rebuild of the image (e.g., to pick up new system dependencies or ensure a clean state), use the `--no-cache` flag:

```bash
docker build --no-cache -t jedy-back .
```

### Debugging & Logs

**View Logs:**
Follow the logs of the running container to see real-time output and errors.

```bash
docker logs -f <container_name_or_id>
# If using compose:
docker compose logs -f back
```

**Access Container Shell:**
To inspect files or run commands inside the running container:

```bash
docker exec -it <container_name_or_id> /bin/bash
# If using compose:
docker compose exec back /bin/bash
```

## Testing

This service includes a comprehensive testing suite built with `pytest`. The tests are located in the `tests` directory and follow a Test-Driven Development (TDD) approach.

To run the tests, use the following command from the project root:

```bash
docker-compose exec back pytest
```

The tests are configured to run against a separate, in-memory SQLite database to ensure test isolation.

## Environment Variables

The application relies on the following environment variables:

- `DATABASE_URL`: Connection string for the PostgreSQL database.
- `API_ENTRYPOINT`: The URL of the external Star Wars API (e.g., `https://swapi.dev/api`).
- `JWT_SECRET`: Secret key used for signing JSON Web Tokens (HS256).
- `ROOT_PATH`: (Optional) The path prefix if the application is served behind a reverse proxy (e.g., `/api`).
- `GOOGLE_API_KEY`: (Optional) API Key for Google Gemini (Text & Image generation).
- `OPENROUTER_API_KEY`: (Optional) API Key for OpenRouter (Text generation fallback).

## Features & Implementation

### Authentication & Security
The backend implements a secure authentication system using **JWT (JSON Web Tokens)**.

- **Library**: `python-jose` for token encoding/decoding.
- **Hashing**: `passlib` with `bcrypt` for secure password hashing.
- **Flow**:
    1. User registers (`/users/signup`), password is hashed and stored.
    2. User logs in (`/users/signin`), receiving a Bearer Token (valid for 30 minutes).
    3. Protected routes (like AI Chat) require the token in the `Authorization` header.

### AI Capabilities
The application integrates Generative AI to enhance the user experience.

#### 1. Contextual Chat
- **Route**: `POST /ai/chat` (Protected)
- **Model**: Uses **Gemini 2.5 Flash** (via `GOOGLE_API_KEY`) or falls back to OpenRouter.
- **Logic**: Users can "chat" with any Star Wars character found in the search results. The backend constructs a prompt injecting the character's known details (from SWAPI) to ensure accurate roleplay.

#### 2. Generative Imagery ("Nano Banana")
- **Route**: `GET /ai/image`
- **Model**: Uses **Gemini 2.5 Flash Image** (codenamed "Nano Banana").
- **Logic**:
    - Generates a photorealistic image of the Star Wars entity (Person, Planet, Starship).
    - **Caching**: Generated images are Base64 encoded and stored in the PostgreSQL database (`EntityImage` table) to save costs and improve performance.
    - **Fallback**: If the AI generation fails or is disabled, it gracefully falls back to `pollinations.ai`.

## Development

This service is configured to use a [Dev Container](https://code.visualstudio.com/docs/devcontainers/containers) for a consistent and isolated development environment. To get started:

1. Open this directory (`back`) in VS Code.
2. When prompted, click "Reopen in Container" to launch the Dev Container.
