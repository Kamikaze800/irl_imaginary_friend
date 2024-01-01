from gtts import gTTS

def text_to_speach(mytext):
    language = 'ru'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    print(myobj)
    myobj.save("test1.mp3")

# text_to_speach('Hellow world')