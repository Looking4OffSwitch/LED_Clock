import time
from clock import LEDClock
from downlights import Downlights
from rpi_ws281x import ws, Color

def main():
    clock = LEDClock(led_segments=32, leds_per_segment=9, pin=18, freq=800000, dma=10,
                     brightness=200, invert=False, channel=0, strip_type=ws.WS2812_STRIP)

    downlights = Downlights(led_cnt=12, pin=13, freq=800000, dma=10, brightness=50,
                            invert=False, channel=1, strip_type=ws.WS2812_STRIP)
    downlights.set_all(Color(128, 128, 128))

    print ('Press Ctrl-C to quit.')

    try:
        while True:
            clock.show_current_time()
            clock.update_second_indicator()
            time.sleep(1)

    finally:
        # This ensures all LEDs are turned off
        del clock
        del downlights

if __name__ == '__main__':
    main()
