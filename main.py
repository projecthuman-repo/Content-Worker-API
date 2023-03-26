from typing import Union

import re
from fastapi import FastAPI
from pydantic import BaseModel
from profanity_check import predict
from contentHandler import contentHandler

# Temporary schema
# Need to work on the instant text verification request schema 
# (may also stay the same)
class InstantTextVerification(BaseModel):
    text: str

class ContentDetails(BaseModel):
    documentID: str
    contentUrl: str
    contentDetails = {}

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
    
# Route to manage queries within the request URL
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}