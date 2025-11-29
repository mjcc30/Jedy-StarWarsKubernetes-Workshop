from contextlib import asynccontextmanager
import os
from fastapi import FastAPI, HTTPException
from .database import create_db_and_tables
from .routes import users, swapi, ai


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before application startup
    create_db_and_tables()
    yield
    # After application shutdown (if needed)


root_path = os.getenv("ROOT_PATH", "")
app = FastAPI(lifespan=lifespan, root_path=root_path)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(swapi.router, prefix="/swapi", tags=["swapi"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])


# Global variable to simulate app health
is_alive = True
version = os.getenv("VERSION", "v1")


@app.get("/")
def read_root():
    if not is_alive:
        raise HTTPException(status_code=500, detail="Internal Server Error (Simulated Crash)")
    return {"message": f"Welcome to the Star Wars API {version}"}


@app.get("/healthz")
def health_check():
    """
    K8s Liveness Probe endpoint.
    If this returns 500, K8s restarts the pod.
    """
    if not is_alive:
        raise HTTPException(status_code=500, detail="Dead")
    return {"status": "alive"}


@app.post("/simulate/crash")
def simulate_crash():
    """
    Toggle the app state to 'dead'.
    """
    global is_alive
    is_alive = False
    return {"status": "crashed", "message": "App is now unhealthy. Liveness probe will fail."}


@app.post("/simulate/heal")
def simulate_heal():
    """
    Toggle the app state to 'alive'.
    """
    global is_alive
    is_alive = True
    return {"status": "healed", "message": "App is now healthy."}
