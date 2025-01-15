import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')

import openai
openai.api_key = OPENAI_KEY

# Function to convert text to speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Initialize the recognizer
r = sr.Recognizer()

def record_text():
    while True:
        try:
            # Use the microphone as source for input
            with sr.Microphone() as source2:
                # Prepare recognizer to receive input
                r.adjust_for_ambient_noise(source2, duration=0.2)
                print("I'm listening...")

                # Listen for user's input
                audio2 = r.listen(source2)

                # Using Google to recognize audio
                Mytext = r.recognize_google(audio2)
                return Mytext

        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except sr.UnknownValueError:
            print("Unknown error occurred. Please try again.")

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5
        )
        message = response['choices'][0]['message']['content']
        messages.append({"role": "assistant", "content": message})
        return message

    except Exception as e:
        return f"An error occurred: {e}"

messages = [{"role": "user", "content": "Act like Ultron from Avengers: Age of Ultron."}]
while True:
    user_text = record_text()
    messages.append({"role": "user", "content": user_text})
    assistant_response = send_to_chatGPT(messages)
    SpeakText(assistant_response)
    print(f"Assistant: {assistant_response}")