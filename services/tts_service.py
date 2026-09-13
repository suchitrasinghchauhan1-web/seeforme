import pyttsx3


def text_to_speech(text):

    # Remove extra spaces
    text = text.strip()

    # Check if text is empty
    if not text:
        return {
            "text": "",
            "message": "No text provided."
        }

    # Start text-to-speech engine
    engine = pyttsx3.init()

    # Speak the text
    engine.say(text)
    engine.runAndWait()

    # Stop the engine
    engine.stop()

    return {
        "text": text,
        "message": "Text spoken successfully."
    }