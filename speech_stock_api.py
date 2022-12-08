# Notes -------------------------------------------------------------------------
# must install the following:
# pip install speechrecognition
# pip install pyttsx3 --user
# -------------------------------------------------------------------------------
# In terminal run: py audio_mic_transcribe.py 
# If transcribed.txt does not exist it will create the file
# Speak into your mic and it will interpret what you said and print to text file
# Listens for a pause to write a new line
# You can edit the text file manually and save at anytime
# -------------------------------------------------------------------------------

import requests
import time
import json
import csv

import speech_recognition
import pyttsx3

api_key = 'ce5q632ad3i4fps3aufgce5q632ad3i4fps3aug0'
stock_list = ['AAPL','AMZN','NFLX','META','GOOG']

# --------------------------------------------------------------------------------------------------------------------------

def get_stock_price(ticker, api_key):
    url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={api_key}"
    request = requests.get(url)
    data = json.loads(request.content)
    print(data)
    return data


    # current_price = data['c']
    # last_close_price = data['pc']
    # round(percentage_change,2)

# def get_most_volatile_stock(stock_list, api_key):
#     # could store all of this in a hashmap / dictionary easily. Code is easier to read this way so left it like this for now.
#     stock_symbol = ""
#     percentage_change = 0
#     max = 0
#     current_price = 0
#     last_close_price = 0
#     # if we were concerned about how many api calls we are doing, and speed efficiency we could do one call with entire stock list
#     for ticker in stock_list:
#         url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={api_key}"
#         request = requests.get(url)
#         data = json.loads(request.content)
#         actual_percentage = (data['c'] - data['pc']) / data['pc'] * 100
#         print(ticker, round(actual_percentage,2), "%") # can comment this out. helpful for seeing that it is working properly
#         if abs(actual_percentage) > max:
#             stock_symbol = ticker
#             percentage_change = actual_percentage
#             max = abs(actual_percentage) # using absolute because you are asking for the largest move up or down
#             current_price = data['c']
#             last_close_price = data['pc']
#     print(stock_symbol, round(percentage_change,2),"%", current_price, last_close_price)
#     # Could have this csv file as a seperate function if you prefer
#     with open('most_volatile_stock.csv', 'w', newline='') as csvfile:
#         fieldnames = ['stock_symbol', 'percentage_change', 'current_price', 'last_close_price']
#         thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         thewriter.writeheader()
#         thewriter.writerow({'stock_symbol' : stock_symbol, 'percentage_change' : , 'current_price' : current_price, 'last_close_price' : last_close_price})



recognizer = speech_recognition.Recognizer()

while True:

    try:

        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            text = recognizer.recognize_google(audio)
            text = text.upper()
            print("Ticker: ", text)

            with open('transcribed.txt', 'a') as f:

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
