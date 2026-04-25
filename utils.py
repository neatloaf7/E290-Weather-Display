import os

ICON_TABLE = [list(range(0,10)), list(range(10,20)), list(range(20,22))]

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

def wmo_handler(code):
    if code == 0:
        return 0
    if 1 <= code <= 3:
        return 1
    if 13 <= code <= 19:
        return 2
    if 10 <= code <= 12 or 40 <= code <= 49:
        return 3
    if 20 <= code <= 29 or 50 <= code <= 59:
        return 4
    if 60 <= code <= 65:
        return 5
    if 80 <= code <= 84:
        return 6
    if 91 <= code <= 92 or code == 95 or 97 <= code <= 98:
        return 7
    if 66 < code <= 69 or 85 <= code <= 90 or 70 <= code <= 79:
        return 8
    if 93 <= code <= 94 or code == 96 or code == 99:
        return 9
    else:
        return 0  