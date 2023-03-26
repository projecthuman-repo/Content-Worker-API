from modules.downloader import downloadFile
from modules.typeFinder import findFileType
from modules.transcriber import transcribeAudio

########################
### FILE DESCRIPTION ###
########################

# This file contains a content handling function that downloads content from 
# a given URL, determines the file type, and performs specific actions based on 
# the type of file. If the content is an audio file, it is sent for transcription 
# using another module called transcriber.

def contentHandler(contentDetails):
    urlToDownload = contentDetails.contentUrl
    downloadResult = downloadFile(urlToDownload)

    downloadedFileType: findFileType(downloadResult)

    if "WAVE" or ".wav" in downloadedFileType:
        print("Audio File Detected - Sending for transcription...")
        transcribeAudio("downloadedFile")