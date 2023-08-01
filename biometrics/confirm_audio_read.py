import whisper
import os 

def read_sentence(sentence, file):
    result = model.transcribe(file)
    stt = result["text"].split()

    errors = 0
    for i, word in enumerate(sentence.split()):
        found = False
        for j in range(-3, 3):
            if (i + j > 0 and i + j < len(stt) and word == stt[i+j]):
                found = True
                break
        if (not found):
            errors += 1

    print(file)
    print(errors)

    return errors <= 5


model = whisper.load_model("base.en")
"""
sentence = "I'm extremely excited for the SHTEM program this year."
for subdir, dirs, files in os.walk("/Users/avrickaltmann/Voice-Authentication-CNN/biometrics/Testing Audio/Yan"):
    for file in files:
        filePath = subdir + "/" + file
        read_sentence(sentence, filePath)
"""