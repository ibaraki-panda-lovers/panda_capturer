import hashlib

import deepl

from movie_to_audio import movie_to_audio
from ami_voice import chinese_audio_to_text_by_ami_voice

def save_video_to_server(uploaded_file, tempfile_dir):
    # Caluculate the hash
    hash = hashlib.md5(uploaded_file.getvalue(), usedforsecurity=False).hexdigest()
    # Save the uploaded file
    movie_path = f"{tempfile_dir}/{hash}_{uploaded_file.name}"
    with open(movie_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    return movie_path, uploaded_file.type

def get_text_zh_jp(movie_path, tempfile_dir, ami_voice_api_key, deepl_api_key):
    # Convert the movie to audio
    audio_path = f"{tempfile_dir}/{hash}.mp3"
    movie_to_audio(movie_path, audio_path, delete_movie=False)

    # Convert the audio to text
    zh_text, code = chinese_audio_to_text_by_ami_voice(
            audio_path,
            ami_voice_api_key,
            delete_audio=True
    )
    if not zh_text:
        return None, None, "AmiVoice", code

    # Translate the text
    translator = deepl.Translator(deepl_api_key)
    try:
        result = translator.translate_text(zh_text, target_lang="JA", source_lang="ZH")
    except Exception as e:
        return None, None, "DeepL", None
    return zh_text, result, None, None
    