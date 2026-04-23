import os
import board
import displayio
import terminalio
import supervisor
import keypad
import wifi
import time
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_display_shapes import line
from classes import MainScreen, Pixel, ForecastScreen, OtherScreen
import adafruit_requests
import adafruit_connection_manager
import utils

def ensure_wifi(pixel):
    if not wifi.radio.connected:
        print("WiFi lost. Reconnecting...")
        pixel.set(color=pixel.RED)
        try:
            wifi.radio.connect(ssid=os.getenv('CIRCUITPY_WIFI_SSID'),
                   password=os.getenv('CIRCUITPY_WIFI_PASSWORD'))
            print("Reconnected!")
            pixel.set(color=pixel.GREEN)
        except Exception as e:
            print(f"Wifi Connection failed: {e}")
            pixel.set(color=pixel.RED)
            return False
    return True

pixel = Pixel()
pixel.set(color=pixel.RED)
print("Connecting to WiFi...")
wifi.radio.connect(ssid=os.getenv('CIRCUITPY_WIFI_SSID'),
                   password=os.getenv('CIRCUITPY_WIFI_PASSWORD'))
print(f"Connected at {wifi.radio.ipv4_address}!")
pixel.set(color=pixel.YELLOW)

pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
requests = adafruit_requests.Session(pool)

#initialize display and main displayio group
display = board.DISPLAY

#import fonts
font0 = terminalio.FONT #small
font1 = bitmap_font.load_font("/fonts/Ari-W9500-11.bdf")
font2 = bitmap_font.load_font("fonts/UAV-OSD-Mono-14.bdf")

#screens
main_screen = MainScreen(font1,font2)
forecast_screen = ForecastScreen(font1)
other_screen = OtherScreen(font1, font2)
screens = [main_screen, forecast_screen, other_screen]

screen_idx = 0

display.root_group = screens[screen_idx].group

weather = utils.get_weather(requests, pixel)

if weather is not None:
    screens[0].update(weather['current'], weather['daily'], weather['hourly'])

time.sleep(1)
display.refresh()
last_refresh = time.monotonic()

key = keypad.KeyMatrix(
        row_pins=(board.IO41,),
        column_pins=(board.IO17,),
        columns_to_anodes=False
)

THRESHOLDS = [(0, pixel.ORANGE), (1, pixel.YELLOW), 
              (2, pixel.GREEN), (4, pixel.RED),
              (7, pixel.WHITE)]

press_time = None
pixel_timeout = 2
refresh_wait = 3
reset_duration = 60

while True:

    keyevent = key.events.get()

    if keyevent:
        print({keyevent})
        
        if keyevent.pressed:
            press_time = time.monotonic()

        if keyevent.released:
            pixel.off()

            #check if ready for update, otherwise do nothing
            if press_time - last_refresh > refresh_wait:
                duration = time.monotonic() - press_time

                #reboot on long hold
                if duration >= 7:
                    supervisor.reload()
                #do nothing if held between 4 and 7 seconds
                #refresh if held between 2 and 4 seconds
                elif 2 <= duration <4:
                    if ensure_wifi(pixel):
                        weather = utils.get_weather(requests, pixel)
                    if weather is not None:
                        screens[screen_idx].update(weather['current'],
                                                weather['daily'], 
                                                    weather['hourly'])
                        display.refresh()
                        last_refresh = time.monotonic()
                #do nothing if held between 1 and 2 seconds
                #go to next screen if held less than 1 second
                elif duration < 1:
                    screen_idx = (screen_idx + 1) % len(screens)
                    if ensure_wifi(pixel):
                        weather = utils.get_weather(requests, pixel)
                    if weather is not None:
                        screens[screen_idx].update(weather['current'],
                                                    weather['daily'], 
                                                    weather['hourly'])
                    display.root_group = screens[screen_idx].group
                    display.refresh()
                    last_refresh = time.monotonic()

            press_time = None

    #colors
    if press_time is not None:
        if press_time - last_refresh > refresh_wait:
            pixel_hold = time.monotonic() - press_time

            for threshold, color in THRESHOLDS:
                if pixel_hold >= threshold:
                    current_color = color
            
            pixel.set(color=current_color)
        
        else:
            pixel.set(color=pixel.RED)

    if screen_idx is not 0:
        if time.monotonic() - last_refresh > reset_duration:
            weather = utils.get_weather(requests, pixel)
            screen_idx = 0
            screens[screen_idx].update(weather['current'],
                                        weather['daily'], 
                                        weather['hourly'])
            display.root_group = screens[screen_idx].group
            display.refresh()
            last_refresh = time.monotonic()
        
    pixel_dt = time.monotonic() - pixel.last_set
    if pixel_dt > pixel_timeout:
        pixel.off()

    pass

