import displayio
import terminalio
import utils
from bmps import (prec, humi, bmp48, bmp72, sunrise, sunset,
                  bmp_background, background_palette, wind)
import time
import neopixel
import board
from adafruit_display_shapes import line, arc
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import wifi

BLACK = 0x000000

class MainBlock:
    def __init__(self, font0=None, font1=None):
        self.group = displayio.Group()
        self.fontmain = font0 or terminalio.FONT
        self.fontalt = font1 or terminalio.FONT


        #main icon setup
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
        self.main_icon[0] = utils.ICON_TABLE[1][4]

        #temps setup
        self.now = label.Label(self.fontalt, text = "--°F", color=BLACK)
        self.high = label.Label(self.fontmain, text = "--°F", color=BLACK)
        self.low = label.Label(self.fontmain, text = "--°F", color=BLACK)
        self.divider = label.Label(self.fontmain, text = "/", color=BLACK)

        self.now.x = 26
        self.now.y = 88

        self.high.anchor_point = (1, 0.5)
        self.high.anchored_position = (37, 104)
        
        self.low.x = 55
        self.low.y = 105
        self.divider.x = 45
        self.divider.y = 105

        

        #precipitation setup
        self.prec_icon = displayio.TileGrid(
                            prec,
                            pixel_shader=prec.pixel_shader,
                            x=5,y=107
                        )
        self.prec_label = label.Label(self.fontmain, text = "--%", color=BLACK)
        self.prec_label.x = 25
        self.prec_label.y = 120

        
        self.group.append(self.prec_icon)
        self.group.append(self.prec_label)

        #humidity setup
        self.humi_icon = displayio.TileGrid(
                            humi,
                            pixel_shader=humi.pixel_shader,
                            x=50,y=110
                        )
        self.humi_label = label.Label(self.fontmain, text = "--%", color=BLACK)
        self.humi_label.x = 70
        self.humi_label.y = 120

        
        self.group.append(self.humi_icon)
        self.group.append(self.humi_label)

        self.line = line.Line(x0=99, x1=99, y0=11, y1=127, color=BLACK)
        self.group.append(self.line)

        self.group.append(self.now)
        self.group.append(self.high)
        self.group.append(self.low)
        self.group.append(self.divider)

    def update(self, current, daily):
        
        row = 1 - int(current['is_day'])
        col = int(current['weather_code'])
        #if wmo == 69-70:
        #    disaster = True
        #col = wmotable[wmo]
        
        #if disaster:
        #    row = 2
        #else:
        #    row = 1 - isday
        self.main_icon[0] = utils.ICON_TABLE[row][col]

        self.now.text = f"{int(current['temperature_2m'])}°F"
        self.high.text = f"{int(daily['temperature_2m_max'][0])}°F"
        self.low.text = f"{int(daily['temperature_2m_min'][0])}°F"
        self.prec_label.text = f"{daily['precipitation_probability_max'][0]}%"
        self.humi_label.text = f"{current['relative_humidity_2m']}%"

class ForecastWidget:
    def __init__(self, font, x, bmp48):
        self.group = displayio.Group(x=x, y=0)
        self.font = font or terminalio.FONT
        self.icon = displayio.TileGrid(
                                 bmp48, 
                                 pixel_shader=bmp48.pixel_shader,
                                 width=1,
                                 height=1,
                                 tile_width=48,
                                 tile_height=48,
                                 x=0,
                                 y=30
                                 )
        
        self.icon[0] = utils.ICON_TABLE[0][9]

        self.temp = label.Label(self.font, text="--°F", x=12, y=84, color=BLACK)

        self.prec = label.Label(self.font, text="--%", x=15, y=102, color=BLACK)
        self.prec_icon = displayio.TileGrid(
                            prec,
                            pixel_shader=prec.pixel_shader,
                            x=-8,y=88)

        self.humi = label.Label(self.font, text="--%", x=15, y=120, color=BLACK)
        self.humi_icon = displayio.TileGrid(
                            humi,
                            pixel_shader=humi.pixel_shader,
                            x=-6,y=108
                        )              

        self.time = label.Label(self.font, text="--:--", x=7, y=24, color=BLACK)

        self.group.append(self.humi_icon)
        self.group.append(self.prec_icon)
        self.group.append(self.icon)
        self.group.append(self.temp)
        self.group.append(self.prec)
        self.group.append(self.humi)
        self.group.append(self.time)

    def update(self, isday, wmo, t, prec, humi, hour):
        row = 1 - isday
        col = wmo

        self.icon[0] = utils.ICON_TABLE[row][col]
        self.temp.text = f"{t}°F"
        self.prec.text = f"{prec}%"
        self.humi.text = f"{humi}%"
        self.time.text = f"{hour}:00"



class StatusBar:
    #tuples for date formatting
    WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    MONTHS = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")

    def __init__(self):
        #make label
        self.time = label.Label(terminalio.FONT, text=f"Sunday, 01 JAN 1970 00:00",
                                                    color=BLACK)
        self.time.anchor_point = (1, 0.5)
        self.time.anchored_position = (280, 4)


        #Location Label
        self.loc = label.Label(terminalio.FONT, text = "San Diego, CA", color=BLACK, x=0, y=4)
        self.topbar  = line.Line(x0=0, x1=295, y0=11, y1=11, color=BLACK)

        #Group
        self.group = displayio.Group()
        self.group.append(self.time)
        self.group.append(self.loc)
        self.group.append(self.topbar)

    def update_time(self, iso_str):
        self.year  = iso_str[0:4]
        self.month = iso_str[5:7]
        self.day   = iso_str[8:10]
        self.hour  = iso_str[11:13]
        self.minute = iso_str[14:16]

        #tuple for getting weekday
        t_tuple = (int(self.year), int(self.month), int(self.day), 
                   int(self.hour), int(self.minute), 0, -1, -1, -1)
        timestamp = time.mktime(t_tuple)
        full_dt = time.localtime(timestamp)
        self.weekday_idx = full_dt.tm_wday

        #Last update time label
        self.time.text = (f"{self.WEEKDAYS[self.weekday_idx]},"
                        f" {self.day} {self.MONTHS[int(self.month)]}"
                        f" {self.year} {self.hour}:{self.minute}")

class MainScreen:
    def __init__(self, font0, font1):
        self.group = displayio.Group()
        
        background = displayio.TileGrid(bmp_background,
                                        pixel_shader=background_palette)
        self.group.append(background)
        
        self.status = StatusBar()
        self.group.append(self.status.group)

        self.main_block = MainBlock(font0, font1)
        self.group.append(self.main_block.group)

        self.forecasts = []
        for i in range(3):
            w = ForecastWidget(font0, 120 + i*60, bmp48)
            self.forecasts.append(w)
            self.group.append(w.group)

    def update(self, current_data, daily_data, hourly_data):
        
        self.main_block.update(current_data, daily_data)
        self.status.update_time(current_data['time'])

        hour = int(current_data['time'][11:13])
        
        for i in range(3):
            idx = hour + (i+1)*2

            wmo = hourly_data['weather_code'][idx]
            isday = hourly_data['is_day'][idx]
            t = int(hourly_data['temperature_2m'][idx])
            prec = hourly_data['precipitation_probability'][idx]
            humi = hourly_data['relative_humidity_2m'][idx]

            self.forecasts[i].update(isday, wmo, t, prec, humi, hourly_data['time'][idx][11:13])
        

class ForecastScreen:
    def __init__ (self, font):
        self.group = displayio.Group()

        background = displayio.TileGrid(bmp_background,
                                pixel_shader=background_palette)
        self.group.append(background)

        self.status = StatusBar()
        self.group.append(self.status.group)

        self.forecasts =[]
        for i in range(5):
            w = ForecastWidget(font, 5+i*60, bmp48)
            self.forecasts.append(w)
            self.group.append(w.group)

    def update(self, current_data, daily_data, hourly_data):
        self.status.update_time(current_data['time'])

        hour = int(current_data['time'][11:13])
        
        for i in range(5):
            idx = hour + (i)*2

            wmo = hourly_data['weather_code'][idx]
            isday = hourly_data['is_day'][idx]
            t = int(hourly_data['temperature_2m'][idx])
            prec = hourly_data['precipitation_probability'][idx]
            humi = hourly_data['relative_humidity_2m'][idx]

            self.forecasts[i].update(isday, wmo, t, prec, humi, hourly_data['time'][idx][11:13])

class OtherScreen:
    def __init__(self, font0, font1):
        self.group = displayio.Group()

        background = displayio.TileGrid(bmp_background,
                                pixel_shader=background_palette)
        self.group.append(background)

        self.status = StatusBar()
        self.group.append(self.status.group)

        self.main_block = MainBlock(font0, font1)
        self.group.append(self.main_block.group)

        self.sunrise_icon = displayio.TileGrid(
                                                sunrise,
                                                pixel_shader=sunrise.pixel_shader,
                                                x=102,
                                                y=88
                                                )
        
        self.sunset_icon = displayio.TileGrid(
                                                sunset,
                                                pixel_shader=sunset.pixel_shader,
                                                x=162,
                                                y=88
                                                )
        
        self.group.append(self.sunrise_icon)
        self.group.append(self.sunset_icon)

        self.sunrise = label.Label(font0, text = "--:--", color=BLACK, 
                                   anchor_point=(0.5,0.5), anchored_position=(117,120))
        self.sunset = label.Label(font0, text = "--:--", color=BLACK, 
                                   anchor_point=(0.5,0.5), anchored_position=(177,120))
        self.group.append(self.sunrise)
        self.group.append(self.sunset)

        self.sun_line = arc.Arc(x=147, y=143, radius=50, direction=90, angle=37, 
                                segments=10, arc_width=2, fill=BLACK)
        self.group.append(self.sun_line)

        self.wind_icon = displayio.TileGrid(
                                            wind,
                                            pixel_shader=wind.pixel_shader,
                                            x = 101,
                                            y = 15
                                        )
        self.group.append(self.wind_icon)

        self.wind = label.Label(font0, text = "-- / -- mph", x=132, y=33, color=BLACK)
        self.group.append(self.wind)

        self.feels = label.Label(font0, text = "Feels like: --°F", x=107, y=63, color=BLACK)
        self.group.append(self.feels)

        self.uv = label.Label(font0, text = "UV Index: --.--", anchor_point = (1,0.5),
                              anchored_position=(296,32), color=BLACK)
        self.group.append(self.uv)

        self.ip = label.Label(font0, text = f"ip:{wifi.radio.ipv4_address}", 
                              anchor_point = (1,0.5),
                              anchored_position=(295,120), 
                              color=BLACK)
        self.group.append(self.ip)

    def update(self, current_data, daily_data, hourly_data):
        
        self.main_block.update(current_data, daily_data)
        self.status.update_time(current_data['time'])
        self.sunrise.text = f"{daily_data['sunrise'][0][11:16]}"
        self.sunset.text = f"{daily_data['sunset'][0][11:16]}"
        self.wind.text = f"{daily_data['wind_speed_10m_max'][0]} / {daily_data['wind_gusts_10m_max'][0]} mph"
        self.feels.text = f"Feels like: {int(current_data['apparent_temperature'])}°F"
        self.uv.text = f"UV Index: {daily_data['uv_index_max'][0]}"

class Pixel:

    RED = (255, 0, 0)
    ORANGE = (255, 127, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    OFF = (0,0,0)

    def __init__(self):
        self.pixel = pixel = neopixel.NeoPixel(board.IO45, 1, brightness=0.3)
        self.pixel.fill(self.OFF)
        self.last_set = time.monotonic()

    def set(self, color=None, brightness=None):
        if color is not None:
            self.pixel.fill(color)

        if brightness is not None:
            self.pixel.brightness = brightness
        
        self.last_set = time.monotonic()
    
    def off(self):
        self.pixel.fill(self.OFF)
        self.is_off = True
