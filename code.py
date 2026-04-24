import os
import board
import terminalio
import supervisor
import keypad
import wifi
import time
import alarm
import displayio
from adafruit_bitmap_font import bitmap_font
from classes import MainScreen, Pixel, ForecastScreen, OtherScreen
import adafruit_requests
import adafruit_connection_manager
import utils
import digitalio
import analogio

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

def sleep_handler():
    global screen_idx, last_action, last_refresh, press_time, key, weather, bat
    #light sleep
    print("sleepin")
    key.deinit()
    light_alarm = alarm.time.TimeAlarm(
                   monotonic_time=time.monotonic() + light_sleep_time)
    #init pins for alarm
    
    pin_alarm = alarm.pin.PinAlarm(pin=board.IO17, value=False, pull=True)
    #sleep here
    alarm.light_sleep_until_alarms(light_alarm, pin_alarm)
    #wake here
    #reinit key
    key = keypad.Keys(
        pins=(board.IO17,),
        value_when_pressed=False,
        pull=True)

    #check if pin alarm, set press time
    if isinstance(alarm.wake_alarm, alarm.pin.PinAlarm):
        print("it was a pin alarm")
        press_time = time.monotonic()
        last_action = press_time
    #after light sleep duration check if screen needs to be reset to 0
    else:
        print("it was a time alarm")
        if screen_idx is not 0:
            screen_idx = 0
            weather = utils.get_weather(requests, pixel)
            if weather is not None:
                screens[screen_idx].update(weather['current'],
                                    weather['daily'], 
                                    weather['hourly'],
                                    utils.get_voltage(bat))
            
            display.root_group = screens[screen_idx].group
            display.refresh()
            last_refresh = time.monotonic()
            last_action = last_refresh
        #if screen 0, deep sleep after light sleep
        else:
            minute = int(weather['current']['time'][14:16])
            sleep_mins = 60 - minute
            deep_sleep_time = sleep_mins * 60
            deep_alarm = alarm.time.TimeAlarm(
            monotonic_time=time.monotonic() + deep_sleep_time)
            #init pin for alarm
            print(f"deep sleep time: {deep_sleep_time}")
            key.deinit()
            pin_alarm = alarm.pin.PinAlarm(pin=board.IO17, 
                                            value=False, pull=True)
            #sleep
            print("deep sleepin")
            alarm.exit_and_deep_sleep_until_alarms(deep_alarm, pin_alarm)

#neopixel
pixel = Pixel()
pixel.set(color=pixel.RED)
key = keypad.Keys(
        pins=(board.IO17,),
        value_when_pressed=False,
        pull=True)

#battery voltage
bat = analogio.AnalogIn(board.BATTERY)
print(f"bat value = {utils.get_voltage(bat)}")

#import fonts
font0 = terminalio.FONT #small
font1 = bitmap_font.load_font("/fonts/Ari-W9500-11.bdf")
font2 = bitmap_font.load_font("fonts/UAV-OSD-Mono-14.bdf")

#initialize display
display = board.DISPLAY

#screens
main_screen = MainScreen(font1,font2)
forecast_screen = ForecastScreen(font1)
other_screen = OtherScreen(font1, font2)
screens = [main_screen, forecast_screen, other_screen]
screen_idx = 0
display.root_group = screens[screen_idx].group

#wifi
print("Connecting to WiFi...")
wifi.radio.connect(ssid=os.getenv('CIRCUITPY_WIFI_SSID'),
                   password=os.getenv('CIRCUITPY_WIFI_PASSWORD'))
print(f"Connected at {wifi.radio.ipv4_address}!")
pixel.set(color=pixel.YELLOW)

pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
requests = adafruit_requests.Session(pool)

weather = utils.get_weather(requests, pixel)
if weather is not None:
    screens[0].update(weather['current'], weather['daily'],
                       weather['hourly'], utils.get_voltage(bat))

display.refresh()
last_refresh = time.monotonic()

press_time = None
pixel_timeout = 2
refresh_wait = 3
light_timeout = 5
last_action = time.monotonic()
light_sleep_time = 60
deep_sleep_time = 3600

THRESHOLDS = [(0, pixel.ORANGE), (1, pixel.YELLOW), 
              (2, pixel.GREEN), (4, pixel.RED),
              (7, pixel.WHITE)]



while True:
    
    #check key
    keyevent = key.events.get()
    if keyevent:
        last_action = time.monotonic()
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
                                                    weather['hourly'],
                                                    utils.get_voltage(bat))
                        display.refresh()
                        last_refresh = time.monotonic()
                        last_action = last_refresh
                #do nothing if held between 1 and 2 seconds
                #go to next screen if held less than 1 second
                elif duration < 1:
                    screen_idx = (screen_idx + 1) % len(screens)
                    if ensure_wifi(pixel):
                        weather = utils.get_weather(requests, pixel)
                    if weather is not None:
                        screens[screen_idx].update(weather['current'],
                                                    weather['daily'], 
                                                    weather['hourly'], 
                                                    utils.get_voltage(bat))
                    display.root_group = screens[screen_idx].group
                    display.refresh()
                    last_refresh = time.monotonic()
                    last_action = last_refresh

            press_time = None
            last_press = time.monotonic()

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
        
    pixel_dt = time.monotonic() - pixel.last_set
    if pixel_dt > pixel_timeout:
        pixel.off()

#sleep timer
    if time.monotonic() - last_action > light_timeout:

        sleep_handler()   

    pass

