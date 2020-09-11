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


"""

@unique
class TimeDigits(Enum):
    """ Maps the 4 digits of a time to a list of their LED segment numbers """
    HOUR_ONE = auto()   # (1)2:59
    HOUR_TWO = auto()   # 1(2):59
    MINUTE_ONE = auto() # 12:(5)9
    MINUTE_TWO = auto() # 12:5(9)

TIME_SEGMENTS = { TimeDigits.HOUR_ONE:   [8,  0,  0,  0,  0,  9,  0],
                  TimeDigits.HOUR_TWO:   [26, 6, 23, 24, 11, 25, 21],
                  TimeDigits.MINUTE_ONE: [30, 4, 27, 28, 13, 29, 19],
                  TimeDigits.MINUTE_TWO: [1,  2, 31, 32, 15, 16, 17]
}

DIGIT_TO_SEGMENT_STATE = {
     # segment number
     #   1, 2, 3, 4, 5, 6, 7
   -1:  [0, 0, 0, 0, 0, 0, 0],  # all segments are off
    0:  [1, 1, 1, 1, 1, 1, 0],
    1:  [1, 0, 0, 0, 0, 1, 0],
    2:  [1, 1, 0, 1, 1, 0, 1],
    3:  [1, 1, 0, 0, 1, 1, 1],
    4:  [1, 0, 1, 0, 0, 1, 1],
    5:  [0, 1, 1, 0, 1, 1, 1],
    6:  [0, 1, 1, 1, 1, 1, 1],
    7:  [1, 1, 0, 0, 0, 1, 0],
    8:  [1, 1, 1, 1, 1, 1, 1],
    9:  [1, 1, 1, 0, 1, 1, 1]
}