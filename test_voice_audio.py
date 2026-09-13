import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty("voices")

print("Number of voices:", len(voices))

for voice in voices:
    print("Voice:", voice.id)

engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)

print("Starting voice test...")

engine.say("Hello. This is SeeForMe AI. Text to speech is working.")

engine.runAndWait()

print("Voice test finished.")

engine.stop()