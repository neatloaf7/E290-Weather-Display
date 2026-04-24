import os
import displayio

ICON_TABLE = [list(range(0,10)), list(range(10,20)), list(range(20,22))]

bmp48 = displayio.OnDiskBitmap("/img/sprites48.bmp")

def get_weather(requests, pixel):
    pixel.set(color=pixel.ORANGE)
    print("Getting data...")
    
    try:
        response = requests.get(os.getenv('URL'))

        data = response.json()

        if response.status_code == 200:
            print("Great Success")
            pixel.set(color=pixel.GREEN)
            return data

        else:
            print(f"error: {response.text}")
            pixel.set(color=pixel.RED)

        response.close()

    except Exception as e:
        print(f"Exception: {e}")
        pixel.set(color=pixel.RED)

def get_voltage(bat):
    return bat.value/65536*3.3*4.9