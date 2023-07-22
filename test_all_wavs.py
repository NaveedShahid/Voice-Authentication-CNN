import os
#import voice_auth

wavs = 'Testing Audio Wav'

if (not os.path.exists(wavs)):
    print("No Audio To Test")
    exit()

print(voice_auth.recognize(".\Testing Audio Wav\Lucas\Lucas (Sick)_\\2A SHTEM Voice Sentence.wav"))
