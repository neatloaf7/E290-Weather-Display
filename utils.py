import json
import os

def get_weather(requests):
    print("Connecting...")
    
    try:
        response = requests.get(os.getenv('URL'))

        data = response.json()

        if response.status_code == 200:
            print("Great Success")
            return data

        else:
            print(f"error: {response.text}")
            return None

        response.close()

    except Exception as e:
        print(f"Exception: {e}")