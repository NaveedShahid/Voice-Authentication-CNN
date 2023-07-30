import os

rootDir = 'Testing Audio'
convertDir = 'Testing Audio Wav'

print("If this doesn't work, you need to install ffmpeg")

if (not os.path.exists(convertDir)):
    os.mkdir(convertDir)

fileCount = 0
for subdir, dirs, files in os.walk(rootDir):
    for dir in dirs:
        dirPath = subdir + "\\" + dir
        newDirPath = convertDir + dirPath[len(rootDir):]
        if (not os.path.exists(newDirPath)):
            os.mkdir(newDirPath)

    for file in files:
        fileCount += 1
        filePath = subdir + "\\" + file
        newFilePath = convertDir + filePath[len(rootDir):len(filePath) - 3] + "wav"
        if (file.endswith('m4a')):
            os.system(f"ffmpeg -i \".\{filePath}\" -ac 2 -f wav \".\{newFilePath}\" -y")
        elif (file.endswith('mp3')):
            os.system(f"ffmpeg -i \".\{filePath}\" \".\{newFilePath}\" -y")
        elif (file.endswith('wav')):
            os.system(f"copy \".\{filePath}\" \".\{newFilePath}\"")

print(f"Successfully converted {fileCount} files")