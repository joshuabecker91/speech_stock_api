# Notes -------------------------------------------------------------------------
# must install the following:
# pip install speechrecognition
# pip install pyttsx3 --user
# -------------------------------------------------------------------------------
# In terminal run: py speech_stock_api
# If quotes.txt does not exist it will create the file
# Speak into your mic the ticker of the stock you want to get a quote on
# It will log the quote in text file and speak the ticker, price, % change to you
# You can edit the text file manually and save at anytime
# -------------------------------------------------------------------------------

import requests
import time
import json
# import csv

import speech_recognition
import pyttsx3

api_key = 'ce5q632ad3i4fps3aufgce5q632ad3i4fps3aug0'

# --------------------------------------------------------------------------------------------------------------------------

def get_stock_price(ticker, api_key):
    url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={api_key}"
    request = requests.get(url)
    data = json.loads(request.content)
    print(data)
    return data

# --------------------------------------------------------------------------------------------------------------------------

recognizer = speech_recognition.Recognizer()

while True:

    try:

        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            text = recognizer.recognize_google(audio)
            text = text.upper()
            print("Ticker: ", text)

            with open('quotes.txt', 'a') as f:

                data = get_stock_price(text, api_key)
                percentage = (data['c'] - data['pc']) / data['pc'] * 100
                currentPrice = str(data['c'])
                print(f"{text} is trading at {currentPrice} change {round(percentage,2)}%")

                f.writelines(f"{text} {currentPrice} {round(percentage,2)}%" + '\n')
                f.close()

                # Initialize
                engine = pyttsx3.init()
                engine.say(f"{text} is trading at {currentPrice} change {round(percentage,2)} percent")
                engine.runAndWait()

    except speech_recognition.UnknownValueError():

        recognizer = speech_recognition.Recognizer()
        continue
