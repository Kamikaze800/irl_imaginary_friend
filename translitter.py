import speech_recognition as sr

def translitter(filename):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        test = r.recognize_whisper(audio_data, language='ru')
        return test

translitter('sample700.wav')