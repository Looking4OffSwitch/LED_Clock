import time
from datetime import datetime
import pytz
import random

from time_digits import TimeDigits, TIME_SEGMENTS, DIGIT_TO_SEGMENT_STATE

from rpi_ws281x import *

# LED strip configuration:
LEDS_PER_SEGMENT = 9
TOTAL_SEGMENTS   = 32

LED_COUNT      = LEDS_PER_SEGMENT * TOTAL_SEGMENTS # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (Between 1 and 14)
LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # 0 or 1
LED_STRIP      = ws.WS2812_STRIP


class LEDClock():

    _BLACK_COLOR = Color(0, 0, 0)
    _SECOND_INDICATOR_COLOR = Color(10, 10, 10)

    def __init__(self, strip, time_zone='America/New_York'):
        self.strip = strip
        self.clear()

        # blinks on and off each second seconds
        self.second_indicator_segment = 20
        self.second_indicator_is_on = False

        self.cur_timezone = pytz.timezone(time_zone)

        self.hour1 = None
        self.hour2 = None
        self.min1 = None
        self.min2 = None

    def second_indicator_pulse(self):
        if self.second_indicator_is_on:
            # Turn it off
            strip.setPixelColor(middle_led_index, self._BLACK_COLOR)
            self.second_indicator_is_on = False
        else:
            # Turn it on
            strip.setPixelColor(middle_led_index, self._SECOND_INDICATOR_COLOR)
            self.second_indicator_is_on = True

        self.strip.show()

    def updated_second_indicator(self):
        if self.second_indicator_is_on:
            # Turn it off
            self.clear_segment(self.second_indicator_segment, True)
            self.second_indicator_is_on = False
        else:
            # Turn it on
            self.light_segment(self.second_indicator_segment, self._SECOND_INDICATOR_COLOR, True)
            self.second_indicator_is_on = True

    def show_current_time(self):
        # zero padded, 12 hr format (e.g. 10:50 or 04:32)
        dt_str = datetime.now(self.cur_timezone).strftime('%I:%M')
        print(dt_str)

        hour1, hour2, min1, min2 = self._split_time(dt_str)
        print(hour1, hour2, min1, min2)

        if self.hour1 != hour1:
            self.hour1 = hour1

            if hour1 == 0:
                self._clear_digit(TimeDigits.HOUR_ONE)
            else:
                self._show_time_helper(TimeDigits.HOUR_ONE, hour1, Color(0, 0, 220))

        if self.hour2 != hour2:
            self.hour2 = hour2
            self._clear_digit(TimeDigits.HOUR_TWO)
            self._show_time_helper(TimeDigits.HOUR_TWO, hour2, Color(0, 0, 220))

        if self.min1 != min1:
            self.min1 = min1
            self._clear_digit(TimeDigits.MINUTE_ONE)
            self._show_time_helper(TimeDigits.MINUTE_ONE, min1, Color(0, 0, 220))

        if self.min2 != min2:
            self.min2 = min2
            self._clear_digit(TimeDigits.MINUTE_TWO)
            self._show_time_helper(TimeDigits.MINUTE_TWO, min2, Color(0, 0, 220))

    def _split_time(self, dt_str):
        # dt_str: 12 hour time format: ex: '12:49' or '05:12'
        hr1 = int(dt_str[0])
        hr2 = int(dt_str[1])

        min1 = int(dt_str[3])
        min2 = int(dt_str[4])

        return (hr1, hr2, min1, min2)

    def clear(self):
        """ Set the entire strip to black (i.e. "off") """
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, self._BLACK_COLOR)
        strip.show()

    def light_segment(self, segment_num, color = Color(255, 0, 0), show=False):
        index = LEDClock.index_for_segment(segment_num, 0)

        for i in range(index, index + LEDS_PER_SEGMENT):
            self.strip.setPixelColor(i, color)

        if show:
            strip.show()

    def clear_segment(self, segment_num, show=False):
        self.light_segment(segment_num, self._BLACK_COLOR, show)

    def _clear_digit(self, time_digit: TimeDigits):
        for segment in TIME_SEGMENTS[time_digit]:
            self.clear_segment(segment)

    def index_for_segment(segment_num, offset):
        if segment_num > TOTAL_SEGMENTS:
            # print(f"segments({segment_num}) can not be greater than {TOTAL_SEGMENTS}")
            return None

        start_index = segment_num * LEDS_PER_SEGMENT - LEDS_PER_SEGMENT
        return start_index

    def _show_time_helper(self, timeDigit: TimeDigits, digit: int, color: Color):
        on_off_flags = DIGIT_TO_SEGMENT_STATE[digit]

        for idx, segment in enumerate(TIME_SEGMENTS[timeDigit]):
            if segment == 0:
                continue

            if on_off_flags[idx] == 1:
                self.light_segment(segment, color, False)
        strip.show()

if __name__ == '__main__':
    # Create NeoPixel object
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    clock = LEDClock(strip)

    print ('Press Ctrl-C to quit.')

    try:
        while True:
            clock.show_current_time()
            clock.updated_second_indicator()
            time.sleep(1)

    except KeyboardInterrupt:
        clock.clear()
