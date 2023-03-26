from modules.downloader import downloadFile
from modules.typeFinder import findFileType
from modules.transcriber import transcribeAudio

### FILE DESCRIPTION ###
# 

# 
def contentHandler(contentDetails):
    urlToDownload = contentDetails.contentUrl
    downloadResult = downloadFile(urlToDownload)

    downloadedFileType: findFileType(downloadResult)

    if "WAVE" or ".wav" in downloadedFileType:
        print("Audio File Detected - Sending for transcription...")
        transcribeAudio("downloadedFile")