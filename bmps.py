import displayio

_cache = {}

def load_bmp(path):
    if path not in _cache:
        _cache[path] = displayio.OnDiskBitmap(path)
    return _cache[path]

def get_prec():
    return load_bmp("/img/drops.bmp")
def get_humi():
    return load_bmp("/img/drop.bmp")
def get_bmp48():
    return load_bmp("/img/sprites48.bmp")
def get_bmp72():
    return load_bmp("/img/sprites72.bmp")
def get_sunrise():
    return load_bmp("/img/sunrise.bmp")
def get_sunset():
    return load_bmp("/img/sunset.bmp")
def get_wind():
    return load_bmp("/img/wind.bmp")
def get_bats():
    return load_bmp("/img/bat.bmp")

_bg = None
def get_background():
    global _bg
    if _bg is None:
            background_bmp = displayio.Bitmap(296, 128, 1)
            background_palette = displayio.Palette(1)
            background_palette[0] = 0xFFFFFF
            _bg = (background_bmp, background_palette)
    return _bg