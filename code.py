import os
import board
import displayio
import storage
import digitalio
import terminalio
import neopixel
import keypad
import wifi
import time
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_display_shapes import line
from classes import Labels, StatusLabels, MainTemp
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
font2 = bitmap_font.load_font("fonts/Minecraftia-Regular-12.bdf")

#Create 12 pt font labels (currently temp and humidity)
labels = Labels(font1)
status = StatusLabels()
main = MainTemp(font2, font1)

#Create white background
background_bitmap = displayio.Bitmap(296, 128, 1)
palette = displayio.Palette(1)
palette[0] = 0xFFFFFF

# Create a Tilegrid with the background and put in the displayio group
t = displayio.TileGrid(background_bitmap, pixel_shader=palette)
splash.append(t)

#lines
topbar  = line.Line(x0=0, x1=295, y0=11, y1=11, color=BLACK)
divider = line.Line(x0=99, x1=99, y0=11, y1=127, color=BLACK)


#image test
#bitmap = displayio.OnDiskBitmap("/img/wi-cloud.bmp")
#bitpalette = bitmap.pixel_shader
#bitpalette.make_transparent(1)
#cloud = displayio.TileGrid(bitmap, pixel_shader=bitpalette)
#cloud.x = 10
#cloud.y = 12

sprites_bmp = displayio.OnDiskBitmap("/img/sprites.bmp")
bitpalette = sprites_bmp.pixel_shader
bitpalette.make_transparent(1)

sprites = displayio.TileGrid(sprites_bmp, pixel_shader=bitpalette,
                                 width = 1,
                                 height = 1,
                                 tile_width=72,
                                 tile_height=72,
                                 default_tile = 0,
                                 x=10,y=12)

sprite_table = [list(range(0,9)), list(range(10,19)), list(range(20,21))]
sprites[0] = sprite_table[0][7]

smlsprites_bmp = displayio.OnDiskBitmap("img/smlsprites.bmp")
smlsprites = displayio.TileGrid(smlsprites_bmp, pixel_shader=bitpalette,
                                 width = 1,
                                 height = 1,
                                 tile_width=48,
                                 tile_height=48,
                                 default_tile = 0,
                                 x=120,y=20
                                 )

smlsprites[0] = sprite_table[0][3]
#append labels
splash.append(labels.group)
splash.append(status.group)

splash.append(divider)
splash.append(topbar)
splash.append(smlsprites)
splash.append(sprites)
splash.append(main.group)

# Show it
display.root_group = splash

labels.update(temp=70, humi=45)
main.update(
    int(weather['current']['temperature_2m']), 
    int(weather['daily']['temperature_2m_max'][0]), 
    int(weather['daily']['temperature_2m_min'][0])
)

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