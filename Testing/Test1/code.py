import board
import displayio
import digitalio
import terminalio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_display_shapes import line
from classes import Labels, StatusLabels

#initialize display and main displayio group
display = board.DISPLAY
splash = displayio.Group()

BLACK = 0x000000

#import fonts
font0 = terminalio.FONT #small
font1 = bitmap_font.load_font("/fonts/Arial-12.bdf")

#Create 12 pt font labels (currently temp and humidity)
labels = Labels(font1)
status = StatusLabels()

#Create white background
background_bitmap = displayio.Bitmap(296, 128, 1)
palette = displayio.Palette(1)
palette[0] = 0xFFFFFF

# Create a Tilegrid with the background and put in the displayio group
t = displayio.TileGrid(background_bitmap, pixel_shader=palette)
splash.append(t)

#lines
topbar  = line.Line(x0=0, x1=295, y0=11, y1=11, color=BLACK)
divider = line.Line(x0=100, x1=100, y0=11, y1=127, color=BLACK)

#append labels
splash.append(labels.group)
splash.append(status.group)
splash.append(divider)
splash.append(topbar)

# Show it
display.root_group = splash

labels.update(temp=70, humi=45)


display.refresh()
print(status.loc.line_spacing)

# Loop forever so you can enjoy your image
while True:  
    pass

