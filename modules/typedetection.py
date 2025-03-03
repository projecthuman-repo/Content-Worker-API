import aiohttp
from fastapi import APIRouter
import re
import mimetypes
from fastapi import HTTPException

router = APIRouter()

async def type_detection(downloaded_file_path):
    if not re.match(r'^https?://', downloaded_file_path):
        raise ValueError(f"Invalid URL: {downloaded_file_path}")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(downloaded_file_path, timeout=5) as response:
            fileType = response.headers.get('content-type')   #Checking the type with content-type 

            if fileType and fileType.startswith('image'):
                print('Detected file type: jpeg')
                return 'image'
            elif fileType and fileType.startswith('video'):
                print('Detected file type: mp4')
                return 'video'
            else:
                content_disp = response.headers.get('Content-Disposition', '')  # Checking the type with Content-Disposition
                match = re.search(r'filename="([^"]+)"', content_disp)
                if match:
                    filename = match.group(1)
                    guessed_type = mimetypes.guess_type(filename)[0]
                    if guessed_type:
                        if guessed_type.startswith('image'):
                            return 'image'
                        elif guessed_type.startswith('video'):
                            return 'video'
                print('Detected file type: unknown')
                raise HTTPException(status_code=400, detail={"status": "error", "message": "Unknown file type"})