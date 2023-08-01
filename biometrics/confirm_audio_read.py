import whisper
import os 

def read_sentence(sentence, file):
    result = model.transcribe(file)
    stt = result["text"].split()
    sentence = sentence.split() 

    errors = 0
    for i, word in enumerate(sentence):
        found = False
        for j in range(-3, 3):
            if (i + j > 0 and i + j < len(stt) and word == stt[i+j]):
                found = True
                break
        if (not found):
            errors += 1

    return errors <= len(sentence) / 2.0


model = whisper.load_model("base.en")


"""
sentences = ["I'm extremely excited for the SHTEM program this year.", "The quick brown fox jumped over the lazy dog.",
                "The hungry purple dinosaur ate the kind, zingy fox, the jabbering crab, and the mad whale.",
            "With tenure, Suzie'd have all the more leisure for yachting, but her publications are no good.",
            "The beige hue on the waters of the loch impressed all, including the French queen."]


for subdir, dirs, files in os.walk("/Users/avrickaltmann/Voice-Authentication-CNN/biometrics/Testing Audio"):
    for file in files:
        filePath = subdir + "/" + file
        checkmark = False
        for sentence in sentences:
            if (read_sentence(sentence, filePath)):
                checkmark= True
                break
        if (not checkmark):
            print(filePath)
"""
