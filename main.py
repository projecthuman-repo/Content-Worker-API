import re
from typing import Union
from fastapi import FastAPI, UploadFile ,File ,Response, HTTPException
from pydantic import BaseModel
from contentHandler import contentHandler
from typing import Optional
import requests
import os

from modules.typedetection import router as typedetection_router
from modules.image_converter import router as image_converter_router
from modules.video_converter import router as video_converter_router
from modules.video_framespliter import router as video_framespliter_router
from modules.image_moderation import router as  image_moderation_router
from modules.image_ocr import router as  image_ocr_router
from modules.downloader import downloadFile


############
### TODO ###
############

#Add Mongo Support after testing url and local path for files

########################
### FILE DESCRIPTION ###
########################

# This file contains a Python FastAPI web application with three routes: 
# one to validate and moderate text, another to validate and moderate 
# arbitrary content based on its URL, and a third to manage queries within 
# the request URL. The application also includes several Pydantic models 
# for request and response validation.

###########################
### CLASS BASED SCHEMAS ###
###########################

# Simple class for instant verification of text based content
class InstantTextVerification(BaseModel):
    text: str

# Main class containing all the necessary information about 
# content to moderate, with documentID for state management
class ContentDetails(BaseModel):
    documentID: str
    contentUrl: str
    contentDetails: dict
    FileType: Optional[str] = "unknown"

##############
### ROUTES ###
##############
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
    #result = predict([stringToCheck])
    result = "fail"

    # Simple check to see if the check passed or failed
    if (result == [1]):
        return {"result": "fail"}
    else:
        return {"result": "pass"}

    
@app.post("/moderate/file")
async def read_root(request: ContentDetails):
    """Returns a JSON Object
    
    The function validates the contentURL coming from the request for validity, then
    calls the contentHandler to offload the moderation part. Based on the result of
    the regex validator, a JSON object is returned.
    """

    content_url = request.contentUrl
    FileType = request.FileType
    print("Started")
    response = await contentHandler(content_url, FileType)
    return response
    


## Temp Routes for testing type detection and file conversion ##
app.include_router(typedetection_router) ## Check the File type that is being recieved return "Unknown" "Vidoe" or "Image"
app.include_router(image_converter_router) ## Convert the image url to a acceptable type 
app.include_router(video_converter_router) ## Convert the video to a wav for transcrbing
app.include_router(video_framespliter_router) ## Split Video frames from image moderation
app.include_router(image_moderation_router) ## image moderation
app.include_router(image_ocr_router) ## image moderation
############################################################


# Route to manage queries within the request URL
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
