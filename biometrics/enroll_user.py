import os
#import voice_auth

name = 'Lucas'
wavs = f'Training Audio Wav\{name}'

if (not os.path.exists(wavs)):
    print("No Audio To Test")
    exit()

count = 0
for subdir, dirs, files in os.walk(wavs):
    for file in files:
        filePath = subdir + "\\" + file
        os.system(f"python voice_auth.py -t enroll -n {name}{count} -f \".\{filePath}\"")
        count += 1