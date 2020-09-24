from time_digits import LEDPosition, LED_SEGMENTS, CHAR_TO_SEGMENTS_MAP
from rpi_ws281x import Adafruit_NeoPixel, Color


class SegmentedLEDStrip():

    def __init__(self, strip: Adafruit_NeoPixel, num_segments: int, leds_per_segment: int):
        required_leds = num_segments * leds_per_segment

        if strip.numPixels() < num_segments * leds_per_segment:
            raise ValueError(f"LED strip has {strip.numPixels()} pixels but requires {required_leds}")

        self.strip = strip
        self.num_segments = num_segments
        self.leds_per_segment = leds_per_segment

        self._black_color = Color(0, 0, 0)

    def clear(self):
        """ Set the entire strip to black (i.e. "off") """

        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, self._black_color)
        self.strip.show()

    def set_segment_color(self, segment_num: int, color: Color, show = False):
        """ Light up a segment with a given color. """

        if segment_num > self.num_segments:
            raise ValueError(f"Invalid segment number: {segment_num}")

        index = self.index_for_segment(segment_num)

        for i in range(index, index + self.leds_per_segment):
            self.strip.setPixelColor(i, color)

        if show:
            self.strip.show()

    def index_for_segment(self, segment_num):
        if segment_num > self.num_segments:
            raise ValueError(f"Invalid segment number: {segment_num}")

        start_index = segment_num * self.leds_per_segment - self.leds_per_segment
        return start_index

    def clear_char_at(self, led_position: LEDPosition):
        """ Turn off the LEDs at the specified digit position """

        for segment in LED_SEGMENTS[led_position]:
            self.set_segment_color(segment, self._black_color)

    def show_char_at(self, led_position: LEDPosition, char: str, color: Color):
        """ Turn on the LEDs at the specified digit position using digit and color. """

        if char == None or len(char) > 1:
            raise ValueError("char must have length 0")

        on_off_flags = CHAR_TO_SEGMENTS_MAP[char]

        for idx, segment in enumerate(LED_SEGMENTS[led_position]):
            if segment == 0:
                self.set_segment_color(segment, self._black_color)
                continue

            if on_off_flags[idx] == 1:
                self.set_segment_color(segment, color)
            else:
                self.set_segment_color(segment, self._black_color)

        self.strip.show()
