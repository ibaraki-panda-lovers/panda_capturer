import os

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

def upload_video(creds, movie_title, movie_path, mime_type):  
    ext = os.path.splitext(movie_path)[-1]
    try:
        service = build("drive", "v3", credentials=creds)
        name = f"{movie_title}{ext}"
        file_metadata = {"name": name}
        media = MediaFileUpload(movie_path, mimetype=mime_type)
         # pylint: disable=maybe-no-member
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
    except HttpError as error:
        file = None

    return file


def upload_report(creds, movie_title, movie_path, report):  
    text_path = f"{movie_path}.txt"
    with open(text_path, "w") as f:
        f.write(report)
    try:
        service = build("drive", "v3", credentials=creds)
        file_metadata = {"name": f"{movie_title}.txt"}
        media = MediaFileUpload(text_path, mimetype="text/plain")
         # pylint: disable=maybe-no-member
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
    except HttpError as error:
        file = None
    finally:
        os.remove(text_path)
    return file