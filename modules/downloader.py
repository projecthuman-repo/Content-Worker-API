import aiohttp
from fastapi import HTTPException

async def downloadFile(url):
    print("Downloading File From: " + url)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=20) as response:  # Add a timeout
                if response.status == 200:
                    file_path = "downloadedFile"  # Define the path *before* opening the file
                    with open(file_path, "wb") as f:
                        while True:
                            chunk = await response.content.readany()
                            if not chunk:
                                break
                            f.write(chunk)
                    return file_path  # Return the path, not the tuple
                elif response.status == 403:  # Check for Forbidden
                    print(f"Error: Forbidden (403) - Unable to download file from {url}")
                    raise HTTPException(status_code=403, detail="Forbidden: Unable to download file")  # Raise HTTP exception
                else:
                    print(f"Error: Unable to download file from {url}, status code: {response.status}")
                    raise HTTPException(status_code=response.status, detail=f"Download failed: {response.status}") # Raise HTTP exception
    except aiohttp.ClientError as e:
        print(f"Error: Unable to download file from {url}: {e}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")  # Raise HTTP exception
    except Exception as e: # Catch any other exceptions
        print(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    