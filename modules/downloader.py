import urllib.request

# TEST SETUP to download files
# Currently only supports .wav files

# Files are downloaded and stored in the root directory

def downloadAudioFile(url):
    # Pass the download url and assign a filename to it
    urllib.request.urlretrieve(url, "transcript.wav")