import json
import os
import displayio

ICON_TABLE = [list(range(0,10)), list(range(10,20)), list(range(20,22))]
bmp48 = displayio.OnDiskBitmap("/img/sprites48.bmp")

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