import requests 
from config import API_KEY,CITY
from flask import jsonify

def fetch_weather_data(city):
    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

    response=requests.get(url)
    if response.status_code==200:
        return response.json()
    else:
        return jsonify({"error":"Failed to fetch data"})

