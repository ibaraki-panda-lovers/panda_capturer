import os
import requests

def chinese_audio_to_text_by_ami_voice(audio_path, api_key, delete_audio=False, *, profile_words_url_encoded=None):
    url = "https://acp-api.amivoice.com/v1/nolog/recognize"
    d = "grammarFileNames=-a-general-zh"
    if profile_words_url_encoded:
        d += f" profileWords={profile_words_url_encoded}"
    body = {
        "u": api_key,
        "d": d,
    }
    files = {
        "a": open(audio_path, "rb")
    }
    response = requests.post(url, data=body, files=files)
    print("AmiVoice:",response.status_code)
    if response.status_code != 200:
        return None, response.status_code
    try:
        text = response.json()["results"][0]["text"]
        # tokens = response.json()["results"][0]["tokens"]
    except:
        text = None
    if delete_audio:
        os.remove(audio_path)
    return text, response.status_code
   