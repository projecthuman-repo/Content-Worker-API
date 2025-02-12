import magic
import pylibmagic

def findFileType(file):
    mime = magic.Magic(mime=True)
    filetype = mime.from_file(file)
    return filetype.split('/')[0]
