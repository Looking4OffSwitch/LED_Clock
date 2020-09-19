# LED_2_COUNT      = 12     # Number of LED pixels.
# LED_2_PIN        = 13      # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
# LED_2_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
# LED_2_DMA        = 10      # DMA channel to use for generating signal (Between 1 and 14)
# LED_2_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
# LED_2_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
# LED_2_CHANNEL    = 1       # 0 or 1
# LED_2_STRIP      = ws.WS2812_STRIP

from rpi_ws281x import *

class Downlights:

    def __init__(self, led_cnt: int, pin: int, freq: int, dma: int,
                 brightness: int, invert: bool, channel: int, strip_type: int):

        self.strip = Adafruit_NeoPixel(led_cnt, pin, freq, dma, invert, brightness,
                                       channel, strip_type)
        self.strip.begin()
        self.clear_all()

    def __del__(self):
        self.clear_all()

    def set_all(self, color: Color):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def set_downlight(self, index, color):
        self.strip.setPixelColor(i, color)
        self.strip.show()

    def clear_all(self):
        """ Set the entire strip to black (i.e. "off") """
        self.set_all(Color(0, 0, 0))
