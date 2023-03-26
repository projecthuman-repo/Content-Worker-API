import cv2
import asyncio
from PIL import Image
from fastapi import APIRouter, File, UploadFile
from nude import Nude
import io
import requests

import numpy as np


router = APIRouter()

# def classify(image):
#     try:
#         image_data = image.read()
#         nparr = np.fromstring(image_data, np.uint8)
#         img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#         pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#         detector = Nude(pil_img)
#         detector.parse()
#         if detector.result:
#             return {"result": "NSFW"}
#         else:
#             return {"result": "SFW"}
#     except Exception as e:
#         return {"error": str(e)}

# @router.post("/image_moderation")
# async def classify_image(image: UploadFile = File(...)):
#     loop = asyncio.get_event_loop()
#     result = await loop.run_in_executor(None, classify, image.file)
#     return result

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)



# def classify(image):
#     try:
#         pil_img = Image.open(image)
#         detector = Nude(pil_img)
#         detector.parse()
#         if detector.result:
#             return {"result": "NSFW"}
#         else:
#             return {"result": "SFW"}
#     except Exception as e:
#         return {"error": str(e)}

# @router.post("/image_moderation")
# async def classify_image(image_url: str):
#     loop = asyncio.get_event_loop()
#     result = await loop.run_in_executor(None, urllib.request.urlopen, image_url)
#     if result.status != 200:
#         return {"error": "Unable to download image from URL"}
#     result = await loop.run_in_executor(None, classify, result)
#     return result


@router.post("/image_moderation")
async def classify_image(image_url: str):
    try:
        #Download Image
        response = requests.get(image_url)
        image_data = response.content
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
            return {"result": "NSFW"}
        else:
            return {"result": "SFW"}
    except Exception as e:
        return {"error": str(e)}




