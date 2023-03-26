from typing import Union

import re
from fastapi import FastAPI
from pydantic import BaseModel
from profanity_check import predict
from contentHandler import contentHandler

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

@app.get("/")
def read_root():
    # Base route to return the current Version Number
    return "PHC: Content Moderation Server - Version 0.1"

@app.post("/moderate/text")
def read_root(request: InstantTextVerification):
    """Returns a JSON Object
    
    The function parses the string from the request and runs it through the profanity
    checker library, based on the result the approapriate result is returned.
    """

    stringToCheck = request.text
    result = predict([stringToCheck])

    # Simple check to see if the check passed or failed
    if (result == [1]):
        return {"validationResult": False}
    else:
        return {"validationResult": True}

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
    
# Route to manage queries within the request URL
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}