import os
import magic


def findFileType(filename):
    if '.' not in filename:
        file_type = magic.from_file(filename)
        print(file_type)
    else:
        file_extension = os.path.splitext(filename)[1]
        print(file_extension)