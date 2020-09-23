from rpi_ws281x import Adafruit_NeoPixel, Color


class SegmentedLEDStrip():

    def __init__(self, strip: Adafruit_NeoPixel, num_segments: int, leds_per_segment: int):
        required_leds = num_segments * leds_per_segment

        if strip.numPixels() < num_segments * leds_per_segment:
            raise ValueError(f"LED strip has {strip.numPixels()} pixels but requires {required_leds}")

        self.strip = strip
        self.num_segments = num_segments
        self.leds_per_segment = leds_per_segment

    def clear(self):
        """ Set the entire strip to black (i.e. "off") """

        black = Color(0, 0, 0)

        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, black)
        self.strip.show()

    def show(self):
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
