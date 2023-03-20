import speech_recognition as sr

# TEST SETUP for the audio transcriber.
# Will need additional setup to work with incoming requests/convert/download audio files appropriately.

def transcribeAudio(audioFileName):
    r = sr.Recognizer()
    
    # use the audio file as the audio source
    with sr.AudioFile(audioFileName) as source:
        # read the entire audio file
        audio = r.record(source)
        transcribed_text = r.recognize_google(audio)

        return transcribed_text