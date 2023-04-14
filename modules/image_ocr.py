import io
from PIL import Image
import httpx
from fastapi import APIRouter
import pytesseract


router = APIRouter()

@router.post("/image_ocr")
async def image_ocr(url: str):
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

        # Convert Image to text 
        text = pytesseract.image_to_string(image)

        #Return Transcribed Text
        return {"text": text}
    
