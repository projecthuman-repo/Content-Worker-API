import io
from PIL import Image
import httpx
from fastapi import FastAPI, Response ,APIRouter

router = APIRouter()

@router.post("/converter/image")
async def image_conversion_to_jpeg(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        # Error responce for not being able to download the image file
        if response.status_code != 200:
            return {"ERROR": "Unable to Download File"}
        
        content_type = response.headers.get("Content-Type")

        # Error responce for url not pointing to an image file
        if not content_type or not content_type.startswith("image/"):
            return {"ERROR": "URL does not contain an image"}
        
        #open image file
        image = Image.open(io.BytesIO(response.content))

        #convert image
        jpeg_image = image.convert("RGB")
        buffer = io.BytesIO()

        #save image as a JPEG
        jpeg_image.save(buffer, format="JPEG")
        buffer.seek(0)

        #Return final converted Image
        return Response(content=buffer.getvalue(), media_type="image/jpeg")
    