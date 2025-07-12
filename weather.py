import requests
import os

def get_weather_data(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return None
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        res = requests.get(url)
        data = res.json()
        if data.get("cod") != 200:
            return None
        return {
            "description": data["weather"][0]["description"].title(),
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
    except Exception as e:
        return None
