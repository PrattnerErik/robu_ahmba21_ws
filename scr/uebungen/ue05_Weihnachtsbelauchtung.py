
https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf
https://pypi.org/project/rpi-ws281x/
https://github.com/rpi-ws281x/rpi-ws281x-python/


import time
from rpi_ws281x import ws, Adafruit_NeoPixel, Color
import argparse

# LED strip configuration:
LED_COUNT = 3        # Number of LED pixels.
LED_PIN = 21          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP = ws.WS2811_STRIP_GRB