import httpx
from fastapi import APIRouter

router = APIRouter()

@router.post("/typedetection")
async def type_detection(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        content_type = response.headers.get('content-type')
    return {"content_type": content_type}