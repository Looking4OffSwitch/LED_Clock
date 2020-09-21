import time
from datetime import datetime
import pytz

from time_digits import TimeDigits, TIME_SEGMENTS, DIGIT_TO_SEGMENTS_MAP

from rpi_ws281x import Adafruit_NeoPixel, Color

class LEDClock():

    def __init__(self, led_strip: Adafruit_NeoPixel, num_segments: int, leds_per_segment:int,
                 digits_color: Color, second_indicator_color: Color,time_zone='America/New_York'):

        self.strip = led_strip
        self.num_segments = num_segments
        self.leds_per_segment = leds_per_segment

        # blinks on and off each second
        self.second_indicator_segment = 20
        self.second_indicator_is_on = False

        self.cur_timezone = pytz.timezone(time_zone)

        self.hour1 = self.hour2 = self.min1 = self.min2 = None

        self._black_color = Color(0, 0, 0)
        self._digits_color = digits_color
        self._second_indicator_color = second_indicator_color

    def __del__(self):
        # Turn off the lights
        self.clear()

    def clear(self):
        """ Set the entire strip to black (i.e. "off") """
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, self._black_color)
        self.strip.show()

    def update_second_indicator(self):
        if self.second_indicator_is_on:
            # Turn it off
            self._set_segment_color(self.second_indicator_segment, self._black_color, True)
            self.second_indicator_is_on = False
        else:
            # Turn it on
            self._set_segment_color(self.second_indicator_segment, self._second_indicator_color, True)
            self.second_indicator_is_on = True
        self.strip.show()

    def show_current_time(self, digits:(int, int, int, int)=None):
        """ digits param used for testing only """

        if digits is None:
            hour1, hour2, min1, min2 = self._get_cur_time_digits()
        else:
            hour1, hour2, min1, min2 = digits
        print(hour1, hour2, min1, min2)

        if self.hour1 != hour1:
            self.hour1 = hour1

            if hour1 == 0:
                self._clear_digit(TimeDigits.HOUR_ONE)
            else:
                self._show_time_helper(TimeDigits.HOUR_ONE, hour1)

        if self.hour2 != hour2:
            self.hour2 = hour2
            self._clear_digit(TimeDigits.HOUR_TWO)
            self._show_time_helper(TimeDigits.HOUR_TWO, hour2)

        if self.min1 != min1:
            self.min1 = min1
            self._clear_digit(TimeDigits.MINUTE_ONE)
            self._show_time_helper(TimeDigits.MINUTE_ONE, min1)

        if self.min2 != min2:
            self.min2 = min2
            self._clear_digit(TimeDigits.MINUTE_TWO)
            self._show_time_helper(TimeDigits.MINUTE_TWO, min2)

    def _get_cur_time_digits(self) -> (int, int, int, int):
        # zero padded, 12 hr format (e.g. 10:50 or 04:32)
        dt_str = datetime.now(self.cur_timezone).strftime('%I:%M')
        # print(dt_str)

        hr1 = int(dt_str[0])
        hr2 = int(dt_str[1])

        min1 = int(dt_str[3])
        min2 = int(dt_str[4])

        return (hr1, hr2, min1, min2)

    def _set_segment_color(self, segment_num: int, color: Color, show = False):
        index = self._index_for_segment(segment_num, 0)

        for i in range(index, index + self.leds_per_segment):
            self.strip.setPixelColor(i, color)

        if show:
            self.strip.show()

    def _clear_digit(self, time_digit: TimeDigits):
        for segment in TIME_SEGMENTS[time_digit]:
            self._set_segment_color(segment, self._black_color)

    def _index_for_segment(self, segment_num, offset):
#TODO error check
        if segment_num > self.num_segments:
            # print(f"segments({segment_num}) can not be greater than {TOTAL_SEGMENTS}")
            return None

        start_index = segment_num * self.leds_per_segment - self.leds_per_segment
        return start_index

    def _show_time_helper(self, timeDigit: TimeDigits, digit: int):
        on_off_flags = DIGIT_TO_SEGMENTS_MAP[digit]

        for idx, segment in enumerate(TIME_SEGMENTS[timeDigit]):
            if segment == 0:
                continue

            if on_off_flags[idx] == 1:
                self._set_segment_color(segment, self._digits_color, False)
        self.strip.show()
