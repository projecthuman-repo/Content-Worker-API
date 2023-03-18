import urllib.request

# TEST SETUP to download files
# Currently manually have to assign a filename. WIP..

# Files are downloaded and stored in the root directory

def downloadFile(url):
    # Pass the download url and assign a filename to it
    urllib.request.urlretrieve(url, "transcript.wav")