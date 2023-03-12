from typing import Union
from fastapi import FastAPI, UploadFile ,File ,Response
from profanity_check import predict
from pydantic import BaseModel

import numpy as np
from PIL import Image
import io
from moviepy.editor import VideoFileClip
import shutil

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

#Recieve a POST request with a file
#check filetype for the uploaded file
#and returns the file type
@app.post("/typedetection")
def type_detection(file : UploadFile= File(...)):
   return {"file": file.content_type}


#Recieve a POST request with a file
#recheck if its an image
#once confirmed convert the image file to a JPEG
#and returns the converted JPEG file
@app.post("/converter/image")
def image_conversion_to_jpeg(file : UploadFile= File(...)):  
      
      if file.content_type.split("/")[0].lower() != "image":
        return {"error": "file is not an image."}
      
      image=Image.open(file.file)
      jpeg_image =image.convert("RGB")
      buffer = io.BytesIO()
      jpeg_image.save(buffer,format="JPEG")
      buffer.seek(0)
      return Response(content=buffer.getvalue(), media_type="image/jpeg")

#Recieve a POST request with a file
#Recheck if the file type is video
#Once confirmed convert the video file to a wav for transcribing
#And returns the converted wav file
@app.post("/converter/video")
async def video_conversion_to_wav(file: UploadFile = File(...)):
   
   if file.content_type.split("/")[0].lower() != "video":
        return {"error": "file is not an video."}
   
   with open("temp.mp4", "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)
    video = VideoFileClip("Original.mp4")

    # Extract the audio from the video and save it to a WAV file
    audio = video.audio
    audio.write_audiofile("Converted.wav")

    # Return the WAV file
    return Response("Converted.wav")
   

# Route to manage queries within the request URL
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}