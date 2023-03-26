import os
import magic

### MODULE DESCRIPTION ###
# Figures out the extension or the file type

# Based on the filename passed as argument, this method checks whether the file 
# currently has a type, if so return that, otherwise we use the magic library to 
# detect the correct file type to return.
def findFileType(filename):
    file_type: str

    # check if file has an extension
    if '.' not in filename:
        # determine file type based on contents
        file_type = magic.from_file(filename)
    else:
        # get the file extension
        file_type = os.path.splitext(filename)[1]
    
    return file_type