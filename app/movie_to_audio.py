# 動画を音声に変換する
import os
import moviepy.editor as mp

def movie_to_audio(movie_path, audio_path, delete_movie=False):
    clip = mp.VideoFileClip(movie_path)
    clip.audio.write_audiofile(audio_path)
    if delete_movie:
        os.remove(movie_path)
