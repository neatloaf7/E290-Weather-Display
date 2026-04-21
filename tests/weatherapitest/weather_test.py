import os
from dotenv import load_dotenv
import requests
import json

#Load API key from .env file
load_dotenv()
API_URL = "https://api.open-meteo.com/v1/forecast"

LAT = 32.7157  # San Diego
LON = -117.1611

# Function to get weather data
def get_weather(lat, lon): 

    #parameters for open meteo api call
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "precipitation_probability", 
                   "weathercode"],
        "daily": ["weathercode", "temperature_2m_max", "temperature_2m_min",
                   "sunrise", "sunset"],
        "current_weather": True,
        "temperature_unit": "fahrenheit",  
        "timezone": "auto",
        "forecast_days": 3
    }
    
    #Request data from OWM API
    response = requests.get(url)

    #Save response as JSON
    filename = "weatherdata.json"
    with open(filename, 'w') as f:
        json.dump(response.json(), f, indent=4)

get_weather()


