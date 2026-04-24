# E290-Weather-Display
Weather Display based on the Heltec Vision Master E290. Written in circuitpython. Icons taken from lmarzen's [ESP32 weather display](https://github.com/lmarzen/esp32-weather-epd) (a good project to check out).

<img width="535" height="403" alt="PXL_20260424_204616255" src="https://github.com/user-attachments/assets/1ca4e4bd-3520-47c6-86ee-2bd68b81b381" />

## How it works
Parses json output from (https://open-meteo.com/), a free weather API. The API provides current, hourly, and daily weather variables every 15 minutes.
Icons are (to be) set by the WMO code provided by the API call.

## Hardware
- Heltec Vision Master E290 - An ESP32-S3 development board with an integrated 2.9 inch epaper screen, LoRa module, and onboard battery management.
- One Adafruit Neokey switch breakout board, taken from the [5x6 breakapart matrix](https://www.digikey.com/en/products/detail/adafruit-industries-llc/5157/14652782)
- One button top 18650 cell with a generic plastic battery holder, soldered to a JST PH connector
- 3D printed case

## Screens
- Main screen with current temperature, daily high and low temperature, daily chance of precipitation, and humidity. Also includes 3 forecasts in 2 hour increments from the current hour
  - Main screen updates at the top of every hour automatically
- Extended 5 forecast screen in 2 hour increments
- Screen with current/daily variables, as well as sunrise/sunset time, daily high wind and gust speeds, daily high UV index, and ip address

## Neokey
- Used to interact with display
  - Short press - Cycle through screens
  - 3 second press - Grab new API response and refresh current screen
  - 5 second press - Cancel action
  - 7 second press - Soft reboot (similar to ctrl-D in REPL)
  - 10 second press - Hard reset (similar to pressing hardware reset button or power cycling)
- Neopixel led indicates status
  - Indicates length of press
  - Indicates general status
    - Red - On boot, error, or too soon after refresh (within 4s)
    - Orange - getting data
    - Green - data
    - Blue - no WiFi connection
    - White - release to soft reboot
    - Yellow - release to hard reset
   
## Main Logic
- Wait for key press, change Neopixel color and perform action according to length of press. Key press interrupts sleep and returns here.
- If no key press has been detected for 10 seconds, go to light sleep (similar to time.sleep()).
- After 60 seconds of light sleep, return to main screen and light sleep again for 60 seconds. If already on main screen, proceed to deep sleep
- Deep sleep until (approximately) the top of the next hour
  - Data is only reported every 15 minutes (i.e. an API request at 10:52 will give the current data for 10:45), so refresh will be within 15 minutes of top of hour
- Refresh screen, then return to top of loop

## Deficiencies
- Long boot up time after deep sleep (5 seconds). Will need to look into optimizing code and bitmap loading
- No way to hit hardware reset button without disassembly. Becomes an issue if an edge case stops code or if usb interface cannot be communicated with (not sure why it does this sometimes)
- Battery voltage to charge remaining calcuation is not good. Will need to test battery performance more

## To do
- Add more pictures
- Add CAD
- Make project page
