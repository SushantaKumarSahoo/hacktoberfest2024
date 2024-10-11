import pyttsx3
import speech_recognition as sr
import pywhatkit
import wikipedia
import datetime
import requests
from decouple import config

# Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}\n")
        except Exception as e:
            print("Say that again please...")
            return "None"
        return command.lower()

def run_jarvis():
    command = take_command()
    if 'play' in command:
        song = command.replace('play', '')
        speak(f'Playing {song}')
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f'Current time is {time}')
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        speak(info)
    elif 'weather' in command:
        city = command.replace('weather in', '')
        api_key = config('WEATHER_API_KEY')
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(url).json()
        weather = response['weather'][0]['description']
        speak(f'The weather in {city} is {weather}')
    else:
        speak('Please say the command again.')

if __name__ == "__main__":
    while True:
        run_jarvis()
