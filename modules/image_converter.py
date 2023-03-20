import io
from PIL import Image
import httpx
from fastapi import FastAPI, Response ,APIRouter

router = APIRouter()

@router.post("/converter/image")
async def image_conversion_to_jpeg(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            return {"error": "failed to download image"}
        content_type = response.headers.get("Content-Type")
        if not content_type or not content_type.startswith("image/"):
            return {"error": "URL does not point to an image"}
        image = Image.open(io.BytesIO(response.content))
        jpeg_image = image.convert("RGB")
        buffer = io.BytesIO()
        jpeg_image.save(buffer, format="JPEG")
        buffer.seek(0)
        return Response(content=buffer.getvalue(), media_type="image/jpeg")