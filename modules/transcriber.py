import speech_recognition as sr

##########################
### MODULE DESCRIPTION ###
##########################

# This file contains a function that uses the speech_recognition library to 
# transcribe an audio file. The function takes the filename of the audio file 
# as input, reads the entire file, and returns the transcribed text using 
# Google's speech recognition API.

async def transcribeAudio(audioFileName):
    r = sr.Recognizer()
    
    try:
        # use the audio file as the audio source
        with sr.AudioFile(audioFileName) as source:
            # read the entire audio file
            audio = r.record(source)
            transcribed_text = r.recognize_google(audio)
            return transcribed_text
        
    except sr.UnknownValueError:
        print("Error: No legible speech exists in this audio file.")
        return "UnknownValueError"