import requests

def yan_speech(text, num):
    key = 'y0_AgAAAABV024iAATuwQAAAAD2nhlf-f4Opn68Tcq8aKtZgKkwNIPU8Fg'
    URL = 'https://tts.voicetech.yandex.net/generate?text='+text+'&format=wav&lang=ru-RU&speaker=ermil&key='+key+'&speed=1&emotion=good'
    response=requests.get(URL)
    if response.status_code==200:
        with open(f'test{num}.mp3','wb+') as file:
            file.write(response.content)
    print(response.status_code)
# def yan_recognize():
#     URL = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'
#     IAM_TOKEN = 'y0_AgAAAABV024iAATuwQAAAAD2nhlf-f4Opn68Tcq8aKtZgKkwNIPU8Fg'
#     ID_FOLDER = 'b1gl5ts3s8hu8fkiv5pd'
#     with open("test.mp3", "rb") as f:
#         test = f.read()
#
#     # в поле заголовка передаем IAM_TOKEN:
#     headers = {'Authorization': f'Bearer {}'}
#
#     # остальные параметры:
#     params = {
#         'lang': 'ru-RU',
#         'folderId': ID_FOLDER,
#         'sampleRateHertz': 48000,
#     }
#
#     response = requests.post(URL_REC, params=params, headers=headers, data=data_sound)
#
#     # бинарные ответ доступен через response.content, декодируем его:
#     decode_resp = response.content.decode('UTF-8')
#
#     # и загрузим в json, чтобы получить текст из аудио:
#
#     text = json.loads(decode_resp)
#
#     return text