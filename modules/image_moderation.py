import cv2
from PIL import Image
from fastapi import APIRouter, File, UploadFile
from nude import Nude
import requests
import aiohttp
import numpy as np

router = APIRouter()

@router.post("/image_moderation")
async def classify_image(image_url: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                image_data = await response.read()
        # Read Image into an numpy array 
        nparr = np.frombuffer(image_data, np.uint8)
        #conver numpy array to an OpenCV Image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        #convert openCV to Pil Image
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        #Run the Nudity Detector with the PIL Image
        detector = Nude(pil_img)
        detector.parse()
        if detector.result:
            return {"NSFW"}
        else:
            return {"SFW"}
    except Exception as e:
        return {"error": str(e)}




