from modules.downloader import downloadFile
from modules.typeFinder import findFileType
from modules.transcriber import transcribeAudio
from modules.image_converter import image_conversion_to_jpeg
from modules.image_moderation import classify_image
from modules.typedetection import type_detection
from modules.video_moderation import predict_video

import requests
from fastapi import FastAPI, UploadFile ,File ,Response, HTTPException
import re, os

########################
### FILE DESCRIPTION ###
########################

# This file contains a content handling function that downloads content from 
# a given URL, determines the file type, and performs specific actions based on 
# the type of file. If the content is an audio file, it is sent for transcription 
# using another module called transcriber.

URLValidationREGEX = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

LOCAL_PATH_REGEX = re.compile(
    r'^[A-Za-z]:(\\|/)(?:[^<>:"/\\|?*]+(\\|/))*[^<>:"/\\|?*]+$|^/([^/\0]+/)*([^/\0]+)$'
)

async def contentHandler(path, FileType):
        print("Path" ,path)
        if FileType == 'unknown':
            if re.match(URLValidationREGEX, path):
                try:
                    FileType = await type_detection(path)
                    print("URL_File Type: ", FileType)
                    file = await downloadFile(path, FileType)
                    print("Downloaded Path ==",file)
                    path = file
                except requests.exceptions.RequestException as e:
                    raise HTTPException(
                        status_code=400,
                        detail={"status": "error", "message": f"Failed to download file: {str(e)}"}
                    )

            elif re.match(LOCAL_PATH_REGEX, path):
                if not os.path.exists(path):
                    raise HTTPException(status_code=400, detail={"status": "error", "message": "Local file does not exist"})  

                FileType = findFileType(path)
                print("Local_File: ", FileType)
        

        if FileType == "image":
            print("Processing Image...")
            moderation_result = classify_image(path)
            print("Image Moderation Result:", moderation_result)
            return moderation_result

        elif FileType == "video":
            print("Processing Video...")            
            moderation_result = await predict_video(path)
            print("Image Moderation Result:", moderation_result)
            return moderation_result
        
        else:
            print("Unsupported file type.")
            raise HTTPException(status_code=401, detail={"status": "error", "message": "Detected file type: unknown"})  

