from typing import Union
from fastapi import FastAPI, UploadFile ,File ,Response
from pydantic import BaseModel
from profanity_check import predict

from modules.typedetection import router as typedetection_router
from modules.image_converter import router as image_converter_router
from modules.video_converter import router as video_converter_router
from modules.video_framespliter import router as video_framespliter_router

# Temporary schema
# Need to work on the instant text verification request schema 
# (may also stay the same)
class InstantTextVerification(BaseModel):
    text: str
app = FastAPI()

# Base route returning an object of hello world
@app.get("/")
def read_root():
    return "PHC: Content Moderation Server - Version 0.1"

# Receives a POST request with a text payload, performs a moderation 
# check on the text using a machine learning model (via the predict() function), 
# and returns a pass/fail result based on the model's prediction.
@app.post("/moderate/text")
def read_root(request: InstantTextVerification):
    stringToCheck = request.text
    result = predict([stringToCheck])

    # Simple check to see if the check passed or failed
    if (result == [1]):
        return {"result": "fail"}
    else:
        return {"result": "pass"}

## Temp Routes for testing type detection and file conversion ##
app.include_router(typedetection_router) ## Check the File type that is being recieved
app.include_router(image_converter_router) ## Convert the image url to a acceptable type 
app.include_router(video_converter_router) ## Convert the video to a wav for transcrbing
app.include_router(video_framespliter_router) ## Split Video frames from image moderation
############################################################


# Route to manage queries within the request URL
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}