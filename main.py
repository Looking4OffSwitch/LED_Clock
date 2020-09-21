#!/usr/bin/env python3
# Author: Reed Mangino

import time
from rpi_ws281x import *
from clock import LEDClock

# LED strip configurations:

LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 10      # DMA channel to use for generating signal (try 10)
LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)

MAIN_LEDS_PER_SEGMENT   = 9
MAIN_TOTAL_LED_SEGMENTS = 32
MAIN_LED_COUNT = MAIN_TOTAL_LED_SEGMENTS * MAIN_LEDS_PER_SEGMENT
MAIN_LED_PIN            = 18      # GPIO pin connected to the pixels (18 uses PWM!).
MAIN_LED_BRIGHTNESS     = 255     # Set to 0 for darkest and 255 for brightest
MAIN_LED_CHANNEL        = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

DOWNLIGHT_LED_COUNT      = 12
# GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
DOWNLIGHT_LED_PIN        = 13
DOWNLIGHT_LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
DOWNLIGHT_LED_CHANNEL    = 1       # 0 or 1

def all_on(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def main():
    main_strip = Adafruit_NeoPixel(MAIN_LED_COUNT, MAIN_LED_PIN, LED_FREQ_HZ, LED_DMA,
                                  LED_INVERT, MAIN_LED_BRIGHTNESS, MAIN_LED_CHANNEL)
    downlights = Adafruit_NeoPixel(DOWNLIGHT_LED_COUNT, DOWNLIGHT_LED_PIN, LED_FREQ_HZ,
                                   LED_DMA, LED_INVERT, DOWNLIGHT_LED_BRIGHTNESS, DOWNLIGHT_LED_CHANNEL)

    main_strip.begin()
    downlights.begin()

    digits_color = Color(0, 0, 255)
    second_indicator_color = Color(30, 30, 30)
    clock = LEDClock(main_strip, MAIN_TOTAL_LED_SEGMENTS, MAIN_LEDS_PER_SEGMENT,
                     digits_color, second_indicator_color)

    print ('Press Ctrl-C to quit.')

    try:
        while True:
            clock.show_current_time()
            clock.update_second_indicator()
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    finally:
        # Ensure all downlight LEDs are turned off
        for i in range(downlights.numPixels()):
            downlights.setPixelColor(i, Color(0, 0, 0))
        downlights.show()

if __name__ == '__main__':
    main()
