import os
import shutil
import cv2
import urllib.request
from fastapi import APIRouter, File, UploadFile

router = APIRouter()

@router.post("/video-to-frames")
async def video_to_frames(video_url: str):
    
    # Create the "temp-uploads" directory if it doesn't exist
    if not os.path.exists("temp-uploads"):
        os.makedirs("temp-uploads")

    # Get the filename from the URL
    filename = os.path.basename(video_url)

    # Get the path to save the file to
    file_path = f"temp-uploads/{filename}"

    # Download the video file
    urllib.request.urlretrieve(video_url, file_path)

    # Open the video file
    cap = cv2.VideoCapture(file_path)

    # Get the frames per second (fps) and frame count
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create the output folder if it does not exist
    output_folder = "temp-video-output"
    os.makedirs(output_folder, exist_ok=True)

    # Calculate the frame index to save for each minute
    frames_per_minute = int(fps * 60)
    frames_to_save = range(0, frame_count, frames_per_minute)

    # Loop through the frames and save only the selected frames
    for i in range(frame_count):
        # Read the frame
        ret, frame = cap.read()

        # If the frame was not read successfully, break the loop
        if not ret:
            break

        # If this is a frame to save, save it as an image
        if i in frames_to_save:
            frame_path = f"{output_folder}/frame_{i}.jpg"
            cv2.imwrite(frame_path, frame)

    # Release the video file
    cap.release()

    # Return the number of frames processed
    return {"frames_processed": len(frames_to_save)}