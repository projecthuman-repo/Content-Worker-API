import shutil
import requests
from fastapi import APIRouter, Response
from moviepy.editor import VideoFileClip

router = APIRouter()

@router.post("/converter/video")
async def video_conversion_to_wav(url: str):
    
    # Download the video file from the URL
    response = requests.get(url, stream=True)
    with open("temp.mp4", "wb") as file:
        shutil.copyfileobj(response.raw, file)

    # Load the video file 
    video = VideoFileClip("temp.mp4")

    # Extract the audio from the video and save it to a WAV file
    audio = video.audio
    audio.write_audiofile("Converted.wav")

    # Return the WAV file
    return Response("Converted.wav")
