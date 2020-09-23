import time
from datetime import datetime
import threading
import pytz

from segmented_led_strip import SegmentedLEDStrip

from time_digits import TimeDigits

from rpi_ws281x import Adafruit_NeoPixel, Color

class LEDClock():

    def __init__(self, led_strip: Adafruit_NeoPixel, num_segments: int, leds_per_segment:int,
                 digits_color: Color, second_indicator_color: Color,time_zone='America/New_York'):


        self.strip = SegmentedLEDStrip(led_strip, num_segments, leds_per_segment)

        self.cur_timezone = pytz.timezone(time_zone)

        self.hour1 = self.hour2 = self.min1 = self.min2 = None

        self._black_color = Color(0, 0, 0)
        self._digits_color = digits_color
        self._second_indicator_color = second_indicator_color

        # blinks on and off each second
        self.second_indicator_segment = 20
        self.second_indicator_is_on = False
        self.second_indicator_thread_should_run = True
        self.second_indicator_thread = threading.Thread(target=self.update_second_indicator, daemon=True)
        self.second_indicator_thread.start()

        self.strip.clear() # Ensure we start with all segments turned off

    def stop(self):
        self.strip.clear()

        # Clean up the background thread
        self.second_indicator_thread_should_run = False
        self.second_indicator_thread.join()

    def update_second_indicator(self):
        """ The second indicator blinks once per second. This method runs on a background thread. """
        while self.second_indicator_thread_should_run:
            if self.second_indicator_is_on:
                self.strip.set_segment_color(self.second_indicator_segment, self._black_color, True)
            else:
                self.strip.set_segment_color(self.second_indicator_segment, self._second_indicator_color, True)

            self.second_indicator_is_on = not self.second_indicator_is_on

            time.sleep(1)

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
                self.strip.clear_digit(TimeDigits.HOUR_ONE)
            else:
                self.strip.show_digit(TimeDigits.HOUR_ONE, hour1, self._digits_color)

        if self.hour2 != hour2:
            self.hour2 = hour2
            self.strip.show_digit(TimeDigits.HOUR_TWO, hour2, self._digits_color)

        if self.min1 != min1:
            self.min1 = min1
            self.strip.show_digit(TimeDigits.MINUTE_ONE, min1, self._digits_color)

        if self.min2 != min2:
            self.min2 = min2
            self.strip.show_digit(TimeDigits.MINUTE_TWO, min2, self._digits_color)

    def _get_cur_time_digits(self) -> (int, int, int, int):
        # zero padded, 12 hr format (e.g. 10:50 or 04:32)
        dt_str = datetime.now(self.cur_timezone).strftime('%I:%M')
        # print(dt_str)

        hr1 = int(dt_str[0])
        hr2 = int(dt_str[1])

        min1 = int(dt_str[3])
        min2 = int(dt_str[4])

        return (hr1, hr2, min1, min2)
