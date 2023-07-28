import os
#import voice_auth

wavs = 'Testing Audio Wav\\Yan'
output = 'Output\\Yan1.txt'

if (not os.path.exists(wavs)):
    print("No Audio To Test")
    exit()

if (not os.path.exists(output)):
    file = open(output, "w")
    file.close()

for subdir, dirs, files in os.walk(wavs):
    for file in files:
        filePath = subdir + "\\" + file
        os.system(f"python voice_auth.py -t recognize -f \".\{filePath}\" -o \".\{output}\"")