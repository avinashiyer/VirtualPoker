from enum import Flag, IntEnum, IntFlag, auto, Enum


class Suit(IntEnum):
    SPADE = auto()
    CLUB = auto()
    HEART = auto()
    DIAMOND = auto()


class Values(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Hands(IntFlag):
    PAIR = auto()
    TWO_PAIR = auto()
    THREE_O_KIND = auto()
    STRAIGHT = auto()
    FLUSH = auto()
    FULL_HOUSE = auto()
    FOUR_O_KIND = auto()
    STRAIGHT_FLUSH = auto()
    ROYAL_FLUSH = auto()

    '''
    Idempotently disable a flag
    '''

    def disable_flag(self, flag):
        return self & ~flag

    '''
    Use to eliminate FLUSH, STRAIGHT FLUSH, ROYAL FLUSH
    '''

    def no_flush(self):
        self.disable_flag(Hands.FLUSH)
        self.disable_flag(Hands.STRAIGHT_FLUSH)
        self.disable_flag(Hands.ROYAL_FLUSH)

    '''
    Use to eliminate straights
    '''

    def no_straight(self):
        self.disable_flag(Hands.STRAIGHT)
        self.disable_flag(Hands.STRAIGHT_FLUSH)
        self.disable_flag(Hands.ROYAL_FLUSH)

    @classmethod
    def get_multis(cls):
        # TODO: Move this to points class when implemented
        multis = {
            cls.TWO_PAIR: 2,
            cls.THREE_O_KIND: 3,
            cls.STRAIGHT: 4,
            cls.FLUSH: 6,
            cls.FULL_HOUSE: 9,
            cls.FOUR_O_KIND: 25,
            cls.STRAIGHT_FLUSH: 50,
            cls.ROYAL_FLUSH: 250
        }
        return multis
    
    @classmethod
    def get_strings(cls):
        res = {
            cls.TWO_PAIR:'TWO PAIR',
            cls.THREE_O_KIND:'THREE OF A KIND',
            cls.FOUR_O_KIND:'FOUR OF A KIND',
            cls.STRAIGHT:'STRAIGHT',
            cls.STRAIGHT_FLUSH:'STRAIGHT FLUSH',
            cls.FLUSH:'FLUSH',
            cls.ROYAL_FLUSH:'ROYAL FLUSH',
            cls.FULL_HOUSE:'FULL HOUSE',
            0:'WHOLE LOT OF NOTHING'
        }
        return res
