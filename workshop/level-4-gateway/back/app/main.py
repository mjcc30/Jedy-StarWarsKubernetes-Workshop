from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
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


@app.get("/")
def read_root():
    return {"message": "Welcome to the Star Wars API"}
