import displayio
import terminalio

from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

BLACK = 0x000000

class MainTemp:
    def __init__(self, fontmain=None, fontother=None):
        self.fontmain = fontmain or terminalio.FONT
        self.fontother = fontother or terminalio.FONT

        #Main Temp
        self.now = label.Label(self.fontmain, text = "--°F", color=BLACK)
        self.high = label.Label(self.fontother, text = "--°F", color=BLACK)
        self.low = label.Label(self.fontother, text = "--°F", color=BLACK)
        self.divider = label.Label(self.fontother, text = "/", color=BLACK)

        self.now.x = 28
        self.now.y = 88
        
        self.high.x = 15
        self.high.y = 105

        self.low.x = 55
        self.low.y = 105

        self.divider.x = 45
        self.divider.y = 105

        self.group = displayio.Group()
        self.group.append(self.now)
        self.group.append(self.high)
        self.group.append(self.low)
        self.group.append(self.divider)

    def update(self, tnow, thigh, tlow):
        self.now.text = f"{tnow}°F"
        self.high.text = f"{thigh}°F"
        self.low.text = f"{tlow}°F"

class MainSprites:
    sprite_table = [list(range(0,9)), list(range(10,19)), list(range(20,21))]
    def __init__(self, path72, path48):
        self.group = displayio.Group()

        #main icon setup
        bmp72 = displayio.OnDiskBitmap(path72)
        self.main_icon = displayio.TileGrid(
                                 bmp72, 
                                 pixel_shader=bmp72.pixel_shader,
                                 width = 1,
                                 height = 1,
                                 tile_width=72,
                                 tile_height=72,
                                 default_tile = 0,
                                 x=10,y=12)
        self.group.append(self.main_icon)
        
        #small icon setup
        #Create an empty list for holding objects
        #Create 3 new tile grids with incrementing x position
        #Append grids to list and self.group
        bmp48 = displayio.OnDiskBitmap(path48)
        self.forecast_icons = []
        for i in range(3):
            grid = displayio.TileGrid(
                                 bmp48, 
                                 pixel_shader=bmp48.pixel_shader,
                                 width = 1,
                                 height = 1,
                                 tile_width=48,
                                 tile_height=48,
                                 default_tile = 0,
                                 x=120 + (i*60),y=20
                                 )
            self.forecast_icons.append(grid)
            self.group.append(grid)
        
        self.main_icon[0] = self.sprite_table[0][1]
        self.forecast_icons[1][0] = self.sprite_table[1][4]



class Labels:
    def __init__(self, font=None):
        #set font or fallback to terminalio
        self.font = font or terminalio.FONT
        
        #temp label
        self.temp   = label.Label(self.font, text = "--°F", color=BLACK, line_spacing=1)
        self.temp.x = 120
        self.temp.y = 90

        #humidity label
        self.humi   = label.Label(self.font, text = "--%", color=BLACK)
        self.humi.x = 120
        self.humi.y = 101

        #Labels group
        self.group = displayio.Group()
        self.group.append(self.temp)
        self.group.append(self.humi)

    def update(self, temp=None, humi=None):
        if temp is not None:
            self.temp.text = f"{temp}°F"
        if humi is not None:
            self.humi.text = f"{humi} %"

class StatusLabels:
    #tuples for date formatting
    WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    MONTHS = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")

    def __init__(self, time=None):
        #FOR TESTING WITH NO TIME INPUT
        self.time = time or (2025, 8, 7, 5, 20, 30)

        #Last update time label
        self.lastUpdate = label.Label(terminalio.FONT, text="", x=125, y=4, color=BLACK)
        self.updateTime(self.time)

        #Location Label
        self.loc = label.Label(terminalio.FONT, text = "San Diego, CA", color=BLACK, x=0, y=4)

        #Group
        self.group = displayio.Group()
        self.group.append(self.lastUpdate)
        self.group.append(self.loc)

    def updateTime(self, dt):
        self.lastUpdate.text = f"{self.WEEKDAYS[dt[3]]}, {dt[2]:02d} {self.MONTHS[dt[1]-1]} {dt[0]} {dt[4]:02d}{dt[5]:02d}"