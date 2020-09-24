from enum import Enum, unique, auto


"""

Each 'line' represents a segment. The segments are always in the same order.
Displaying a 1 would light up segments 1 and 6. Displaying an 8 would light up all segments.

           2
        -------
        |     |
    3   |     |  1
        -------
        |  7  |
    4   |     |  6
        -------
           5

Layout (and order) of all segements

       --- POS_4        --- POS_3          --- POS_2           --- POS_1
       |                |                  |                   |
       \/               \/                 \/                  \/

             7          6        5         4         3         2
         --------- --------- --------- --------- --------- ---------
        |         |         |         |         |         |         |
      8 |         |23       |26       |27       |30       |31       | 1
        |         |         |         |         |         |         |
         --------- --------- --------- --------- --------- ---------
        |    22   |    21   |    20   |    19   |    18   |    17   |
      9 |         |24       |25       |28       |29       |32       | 16
        |         |         |         |         |         |         |
         --------- --------- --------- --------- --------- ---------
            10         11        12        13        14        15

    NOTE: POS_4 can only display a "1". It is used for representing a time where the
          hour value (in 12 hr format) is >= 10.
"""

@unique
class LEDPosition(Enum):
    """ Maps the 4 digits of a time to a list of their LED segment numbers """
    POS_1 = auto()   # 123(4)
    POS_2 = auto()   # 12(3)4
    POS_3 = auto()   # 1(2)34
    POS_4 = auto()   # (1)234 - Only valid values are 0 (clear) and 1

# The segments that make up each alpha-num LED digit
LED_SEGMENTS = { LEDPosition.POS_1: [1,  2, 31, 32, 15, 16, 17],
                 LEDPosition.POS_2: [30, 4, 27, 28, 13, 29, 19],
                 LEDPosition.POS_3: [26, 6, 23, 24, 11, 25, 21],
                 LEDPosition.POS_4: [8,  0,  0,  0,  0,  9,  0],
}

# Each array index maps to the LED segment shown in the comment at the top of this file.
CHAR_TO_SEGMENTS_MAP = {
     # segment number
     #    1, 2, 3, 4, 5, 6, 7
    ' ': [0, 0, 0, 0, 0, 0, 0],  # all segments are off

    '0': [1, 1, 1, 1, 1, 1, 0],
    '1': [1, 0, 0, 0, 0, 1, 0],
    '2': [1, 1, 0, 1, 1, 0, 1],
    '3': [1, 1, 0, 0, 1, 1, 1],
    '4': [1, 0, 1, 0, 0, 1, 1],
    '5': [0, 1, 1, 0, 1, 1, 1],
    '6': [0, 1, 1, 1, 1, 1, 1],
    '7': [1, 1, 0, 0, 0, 1, 0],
    '8': [1, 1, 1, 1, 1, 1, 1],
    '9': [1, 1, 1, 0, 1, 1, 1],

    'a': [1, 1, 1, 1, 0, 1, 1],
    'b': [0, 0, 1, 1, 1, 1, 1],
    'c': [0, 1, 1, 1, 1, 0, 0],
    'd': [1, 0, 0, 1, 1, 1, 1],
    'e': [0, 1, 1, 1, 1, 0, 1],
    'f': [0, 1, 1, 1, 0, 0, 1],
    'g': [0, 1, 1, 1, 1, 1, 0],
    'h': [1, 0, 1, 1, 0, 1, 1],
    'i': [0, 0, 1, 1, 0, 0, 0],
    'j': [1, 0, 0, 1, 1, 1, 0],
    'k': [0, 0, 1, 1, 0, 0, 1],
    'l': [0, 0, 0, 0, 0, 0, 0],
    'm': [1, 1, 1, 1, 0, 1, 0],
    'n': [0, 0, 0, 1, 0, 1, 1],
    'o': [0, 0, 0, 1, 1, 1, 1],
    'p': [1, 1, 1, 1, 0, 0, 1],
    'q': [1, 1, 1, 0, 1, 1, 1],
    'r': [0, 0, 0, 1, 0, 0, 1],
    's': [0, 1, 1, 0, 1, 1, 1],
    't': [0, 0, 1, 1, 1, 0, 1],
    'u': [0, 0, 0, 1, 1, 1, 0],
    'v': [1, 0, 1, 1, 1, 1, 0],
    'w': [1, 0, 1, 1, 1, 1, 1],
    'x': [1, 0, 1, 1, 0, 1, 1],
    'y': [1, 0, 1, 0, 1, 1, 1],
    'z': [1, 1, 0, 1, 1, 0, 0],

    '-': [0, 0, 0, 0, 0, 0, 1],
    '_': [0, 0, 0, 0, 1, 0, 0],
    '=': [0, 0, 0, 0, 1, 0, 1],
    '°': [1, 1, 1, 0, 0, 0, 1],
    '(': [0, 1, 1, 1, 1, 0, 0],
    '[': [0, 1, 1, 1, 1, 0, 0],
    ')': [1, 1, 0, 0, 1, 1, 0],
    '}': [1, 1, 0, 0, 1, 1, 0],
    '?': [1, 1, 0, 1, 0, 0, 1],
    '"': [1, 0, 1, 0, 0, 0, 0],
    '\'': [0, 0, 1, 0, 0, 0, 0],
}
