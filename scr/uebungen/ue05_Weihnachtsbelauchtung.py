
# https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf
# https://pypi.org/project/rpi-ws281x/
# https://github.com/rpi-ws281x/rpi-ws281x-python/


import time
from rpi_ws281x import ws, Adafruit_NeoPixel, Color
import argparse

# LED strip configuration:
LED_COUNT = 3        # Number of LED pixels.
LED_PIN = 21          # GPIO pin connected to the pixels (18 uses PWM!).
LED_INVERT = False
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP = ws.WS2811_STRIP_GRB

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
                          LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

strip.begin()

j = 0

colors = [Color(255,0,0),Color(255,255,0),Color(0,255,0)]

while True:
    for i in range(LED_COUNT):#erzeugt werte 0,1,2, für i wenn LED_COUNT == 3
        strip.setPixelColor(i,colors[(i+j)%LED_COUNT])#stellt farbe an led ein
    strip.show()
    j+=1
    j %= LED_COUNT

