from typing import Union

from fastapi import FastAPI
from profanity_check import predict
from pydantic import BaseModel
from modules.downloader import downloadFile

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

# Receives a POST request with a JSON payload, which contains the ContentDetails
# for the content to be moderated, and management of state to return a response
# back whether the URL was valid or not.
# Based on the document ID, it will be currently used to track states and a callback
# method will send the moderated result to the Client-Facing API for DB updates.
@app.post("/moderate")
def read_root(request: ContentDetails):
    urlToDownload = request.contentUrl
    downloadResult = downloadFile(urlToDownload)

    if downloadResult == "downloadedFile":
        return {"response": True}
    else:
        return {"response": False}
    
# Route to manage queries within the request URL
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}