import pandas as pd

def process_weather_data(raw_data):
    if 'error' in raw_data:
        return raw_data
    
    # Extract wind speed and feels like temperature
    wind_speed = raw_data['wind'].get('speed', 'N/A')
    feels_like = raw_data['main'].get('feels_like', raw_data['main']['temp']) - 273.15
    
    processed_data = {
        'city': raw_data['name'],
        'country': raw_data['sys'].get('country', 'N/A'),
        'temperature': round(raw_data['main']['temp'] - 273.15, 2),
        'feels_like': round(feels_like, 2),
        'humidity': raw_data['main']['humidity'],
        'pressure': raw_data['main'].get('pressure', 'N/A'),
        'weather': raw_data['weather'][0]['description'],
        'wind_speed': wind_speed,
        'clouds': raw_data.get('clouds', {}).get('all', 'N/A'),
        'sunrise': raw_data['sys'].get('sunrise', 'N/A'),
        'sunset': raw_data['sys'].get('sunset', 'N/A')
    }
    return processed_data