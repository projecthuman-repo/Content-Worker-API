import urllib.request

### MODULE DESCRIPTION ###
# Downloads a file from a defined URL and stores it in the project's root directory.

# Define a function with a passed in url
def downloadFile(url):
    print("Downloading File From: " + url)

    # Use the urlretrieve method of the urllib.request module to download the file
    # The downloaded file will be saved in the root directory with the name 'downloadedFile' and without an extension
    # The returned tuple contains the path to the newly created data file as well as the resulting HTTPMessage object, if needed.
    try:
        return urllib.request.urlretrieve(url, "downloadedFile")[0]
    except urllib.error.HTTPError:
        print("Error: Unable to download file, invalid URL.")
        return "Invalid Error"