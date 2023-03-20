import os
import magic

### MODULE DESCRIPTION ###
# Figures out the extension or the file type

# Based on the filename passed as argument, this method checks whether the file 
# currently has a type, if so print that, otherwise we use the magic library to 
# detect what type of file it is.
def findFileType(filename):
    # check if file has an extension
    if '.' not in filename:
        # determine file type based on contents
        file_type = magic.from_file(filename)
        print(file_type)
    else:
        # get the file extension
        file_extension = os.path.splitext(filename)[1]
        print(file_extension)