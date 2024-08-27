import speech_recognition as sr

def recognize_speech_from_mic():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Set up the microphone
    with sr.Microphone() as source:
        print("Adjusting for ambient noise. Please wait...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Web Speech API
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print("Sorry, there was an error with the request; {0}".format(e))

if __name__ == "__main__":
    recognize_speech_from_mic()
