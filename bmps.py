import displayio

prec = displayio.OnDiskBitmap("/img/drops.bmp")
humi = displayio.OnDiskBitmap("/img/drop.bmp")
bmp48 = displayio.OnDiskBitmap("/img/sprites48.bmp")
bmp72 = displayio.OnDiskBitmap("/img/sprites72.bmp")
sunrise = displayio.OnDiskBitmap("/img/sunrise.bmp")
sunset = displayio.OnDiskBitmap("/img/sunset.bmp")
wind = displayio.OnDiskBitmap("/img/wind.bmp")

bmp_background = displayio.Bitmap(296, 128, 1)
background_palette = displayio.Palette(1)
background_palette[0] = 0xFFFFFF