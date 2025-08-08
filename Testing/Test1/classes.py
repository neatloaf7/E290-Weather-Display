import displayio
import terminalio

from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

BLACK = 0x000000

class Labels:
    def __init__(self, font=None):
        #set font or fallback to terminalio
        self.font = font or terminalio.FONT
        
        #temp label
        self.temp   = label.Label(self.font, text = "--°F", color=BLACK)
        self.temp.x = 50
        self.temp.y = 100

        #humidity label
        self.humi   = label.Label(self.font, text = "--%", color=BLACK)
        self.humi.x = 50
        self.humi.y = 120

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