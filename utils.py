import json
import os

ICON_TABLE = [list(range(0,9)), list(range(10,19)), list(range(20,21))]

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