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

        self.now.x = 33
        self.now.y = 90
        
        self.high.x = 15
        self.high.y = 100

        self.low.x = 55
        self.low.y = 100

        self.divider.x = 45
        self.divider.y = 100

        self.group = displayio.Group()
        self.group.append(self.now)
        self.group.append(self.high)
        self.group.append(self.low)
        self.group.append(self.divider)

    def update(self, tnow, thigh, tlow):
        self.now.text = f"{tnow}°F"
        self.high.text = f"{thigh}°F"
        self.low.text = f"{tlow}°F"


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