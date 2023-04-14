import aiohttp
from fastapi import APIRouter

router = APIRouter()

async def type_detection(downloadResult):
    url = (await downloadResult)['downloadedFilePath']
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=5) as response:
            fileType = response.headers.get('content-type')
            if fileType.startswith('image'):
                print('Detected file type: jpeg')
                return 'image'
            elif fileType.startswith('video'):
                print('Detected file type: mp4')
                return 'video'
            else:
                print('Detected file type: unknown')
                return 'unknown'
