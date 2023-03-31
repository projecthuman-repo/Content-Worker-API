import os
import magic

##########################
### MODULE DESCRIPTION ###
##########################

# This file contains a module that determines the file type based on the filename 
# passed as an argument, checking whether the file currently has a type or using 
# the magic library to detect the correct file type.

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