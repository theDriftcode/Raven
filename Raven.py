from openai import OpenAI

client = OpenAI(api_key="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")

import speech_recognition as sr
import pyttsx3
import time


# Initialize OpenAI API

# Initialize the text to speech engine
engine = pyttsx3.init()


def transcribe_audio_to_text(filename):
    recogizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recogizer.record(source)
    try:
        return recogizer.recognize_google(audio)
    except:
        print("skipping unknown error")


def generate_response(prompt):
    response = client.completions.create(engine="text-davinci-003",
    prompt=prompt,
    max_tokens=4000,
    n=1,
    stop=None,
    temperature=0.5)
    return response.choices[0].text

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        # Wait for user say "genius"
        print("Say 'Raven' to start recording your question")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "raven":
                    # record audio
                    filename = "input.wav"
                    print("Say your question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    # transcript audio to test
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"you said {text}")

                        # Generate the response
                        response = generate_response(text)
                        print(f"GPT-3 says: {response}")

                        # read resopnse using GPT3
                        speak_text(response)
            except Exception as e:
                print("An error ocurred: {}".format(e))


if __name__ == "__main__":
    main()
