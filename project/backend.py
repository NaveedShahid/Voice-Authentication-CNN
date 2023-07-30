import os
from pydub import AudioSegment
import pathlib

from biometrics.voice_auth import enroll, recognize

def enroll_user(username, audioFilePath):
    if (pathlib.Path(audioFilePath).suffix == ".mp3"):
        audio = AudioSegment.from_file(audioFilePath, format="mp3")
    elif (pathlib.Path(audioFilePath).suffix == ".m4a"):
        audio = AudioSegment.from_file(audioFilePath, format="m4a")
    elif (pathlib.Path(audioFilePath).suffix == ".wav"):
        audio = AudioSegment.from_file(audioFilePath, format="wav") 
    else:
        print('ERROR, FILETYPE NOT SUPPORTED')

    output = os.path.join("project/output", username + ".wav")
    audio.export(output, format="wav")

    enroll(username, output)

def authenticate_user(username, audioFilePath):
    if (pathlib.Path(audioFilePath).suffix == ".mp3"):
        audio = AudioSegment.from_file(audioFilePath, format="mp3")
    elif (pathlib.Path(audioFilePath).suffix == ".m4a"):
        audio = AudioSegment.from_file(audioFilePath, format="m4a")
    elif (pathlib.Path(audioFilePath).suffix == ".wav"):
        audio = AudioSegment.from_file(audioFilePath, format="wav") 
    else:
        print('ERROR, FILETYPE NOT SUPPORTED')

    output = os.path.join("project/output", username + ".wav")
    audio.export(output, format="wav")

    user = recognize(output)
    os.remove(os.path.join("project/output", username + ".wav"))

    return username == user[:-1]