import re
from typing import Union
from fastapi import FastAPI, UploadFile ,File ,Response
from pydantic import BaseModel
from profanity_check import predict
from contentHandler import contentHandler

from modules.typedetection import router as typedetection_router
from modules.image_converter import router as image_converter_router
from modules.video_converter import router as video_converter_router
from modules.video_framespliter import router as video_framespliter_router
from modules.image_moderation import router as  image_moderation_router
from modules.image_ocr import router as  image_ocr_router

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
    result = predict([stringToCheck])

    # Simple check to see if the check passed or failed
    if (result == [1]):
        return {"result": "fail"}
    else:
        return {"result": "pass"}
    

    
@app.post("/moderate")
def read_root(request: ContentDetails):
    """Returns a JSON Object
    
    The function validates the contentURL coming from the request for validity, then
    calls the contentHandler to offload the moderation part. Based on the result of
    the regex validator, a JSON object is returned.
    """
    
    URLValidationREGEX = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if re.match(URLValidationREGEX, request.contentUrl):
        contentHandler(request)
        
        return {"validationResult": True}
    else:
        return {"validationResult": False}




## Temp Routes for testing type detection and file conversion ##
app.include_router(typedetection_router) ## Check the File type that is being recieved
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