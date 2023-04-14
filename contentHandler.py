from modules.downloader import downloadFile
from modules.typeFinder import findFileType
from modules.transcriber import transcribeAudio
from modules.image_converter import image_conversion_to_jpeg
from modules.image_moderation import classify_image

########################
### FILE DESCRIPTION ###
########################

# This file contains a content handling function that downloads content from 
# a given URL, determines the file type, and performs specific actions based on 
# the type of file. If the content is an audio file, it is sent for transcription 
# using another module called transcriber.

def contentHandler(contentDetails):
    urlToDownload = contentDetails.contentUrl
    downloadResult =  downloadFile(urlToDownload)
    downloadedFileType=  findFileType(downloadResult)
    print("Type: ", downloadedFileType)

    if "x-wav" in downloadedFileType:
        print("Audio File Detected - Sending for transcription...")
        transcription =   transcribeAudio(downloadResult)
        print("Transcription: ", transcription)


    elif "image" in downloadedFileType or ".jpeg" in downloadedFileType:
        print("Image File Detected - Processing...")
        convertedimage= image_conversion_to_jpeg(downloadResult)
        results=  classify_image(contentDetails.contentUrl)
        if results!=0:
            print("Image Result:",  results)
        else:
            print("Unable to classify image:", results)
