from fastapi import APIRouter, Depends, HTTPException
import httpx
from ..security import create_access_token
import os
from dotenv import load_dotenv

load_dotenv()

SWAPI_ENTRYPOINT = os.getenv("SWAPI_ENTRYPOINT")

router = APIRouter()


@router.get("/search")
async def search_swapi(resource: str, query: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{SWAPI_ENTRYPOINT}/{resource}/?search={query}"
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.",
            )
