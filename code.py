import os
import board
import displayio
import digitalio
import terminalio
import neopixel
import keypad
import wifi
import time
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_display_shapes import line
from classes import ForecastWidget, MainScreen
import adafruit_requests
import adafruit_connection_manager
import utils

wifi.radio.connect(ssid=os.getenv('CIRCUITPY_WIFI_SSID'),
                   password=os.getenv('CIRCUITPY_WIFI_PASSWORD'))
print(f"Connected to {wifi.radio.ipv4_address} !")

pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)

requests = adafruit_requests.Session(pool)
weather = utils.get_weather(requests)
print(f"{weather['latitude']}")

#initialize display and main displayio group
display = board.DISPLAY
splash = displayio.Group()

BLACK = 0x000000

#import fonts
font0 = terminalio.FONT #small
font1 = bitmap_font.load_font("/fonts/Ari-W9500-11.bdf")
font2 = bitmap_font.load_font("fonts/UAV-OSD-Mono-14.bdf")

#Create 12 pt font labels (currently temp and humidity)

#Create white background
background_bitmap = displayio.Bitmap(296, 128, 1)
palette = displayio.Palette(1)
palette[0] = 0xFFFFFF

# Create a Tilegrid with the background and put in the displayio group
t = displayio.TileGrid(background_bitmap, pixel_shader=palette)
splash.append(t)

main_screen = MainScreen(font1,font2)

#append labels
splash.append(main_screen.group)


# Show it
display.root_group = splash

main_screen.main_block.update(int(weather['current']['is_day']),
                    7,
                    int(weather['current']['temperature_2m']), 
                    int(weather['daily']['temperature_2m_max'][0]), 
                    int(weather['daily']['temperature_2m_min'][0]),
                    int(weather['daily']['precipitation_probability_max'][0]),
                    int(weather['current']['relative_humidity_2m']),
)

main_screen.update_forecasts(int(weather['current']['time'][11:13]), weather['hourly'])
main_screen.status.update_time(weather['current']['time'])
display.refresh()
ptest = 4
ftest = (
    "hello \n"
    f"this is" 
    f"a test"
    )

print(ftest)

key = keypad.KeyMatrix(
        row_pins=(board.IO41,),
        column_pins=(board.IO17,),
        columns_to_anodes=False
)
#col = digitalio.DigitalInOut(board.IO17)
#col.direction = digitalio.Direction.OUTPUT
#col.value = False

#row = digitalio.DigitalInOut(board.IO41)
#row.direction = digitalio.Direction.INPUT
#row.pull = digitalio.Pull.UP

pixel = neopixel.NeoPixel(board.IO45, 1, brightness=0.3)

COLORS = [
        (0.0, (255,0,0)),
        (1.0, (255,255,0)),
        (2.0, (0,255,0)),
        (5.0, (255,0,0)),
]


#button = digitalio.DigitalInOut(board.BUTTON0)
#button.pull = digitalio.Pull.UP

# Loop forever so you can enjoy your image
press_time = None
while True:

    keyevent = key.events.get()

    if keyevent:
        print({keyevent})
        
        if keyevent.pressed:
            pixel.fill((0,0,255))
            press_time = time.monotonic()
            
        if keyevent.released:
            pixel.fill((0,0,0))
            press_time = None

    if press_time is not None:
        duration = time.monotonic() - press_time

        current_color = (0,0,0)
        for threshold, color in COLORS:
            if duration >= threshold:
                current_color = color
        
        pixel.fill(current_color)
              
    #if row.value == 1:
    #    print("1")
    #    pixel.fill((0,0,0))
    #else:
    #    print("0")
    #    pixel.fill((0,255,0))

    pass