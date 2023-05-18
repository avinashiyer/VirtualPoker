from itertools import product
from random import shuffle
from card_enums import Suit,Values

SPADE = """\
|       /\     |
|     .'  `.   |
|   .'      '. |
|  {____||____}|
|       ||     |"""

CLUB = """\
|       .~.    |
|      (___)   |
|    .~.   .~. |
|   (___) (___)|
|       |||    |"""


HEART = """\
|   .-~-_-~-.  |
| {           }|
|  `.       .' |
|    `.   .'   |
|      \ /     |"""

DIAMOND = """\
|         /\   |
|       .`  '. |
|      <      >|
|       `.  .' |
|         \/   |"""

BOUNDRY = "+──────────────+"

ACE = """\
|     /\       |
|    /  \      |
|   / /\ \     |
|  / ____ \    |
| /_/    \_\   |
|              |"""

KING = """\
|  _  __       |
| | |/ /       |
| | ' /        |
| |  <         |
| | . \        |
| |_|\_\       |"""

QUEEN = """\
|   ____       |
|  / __ \      |
| | |  | |     |
| | |  | |     |
| | |__| |     |
|  \___\_\     |"""

JACK = """\
|       _      |
|      | |     |
|      | |     |
|  _   | |     |
| | |__| |     |
|  \____/      |"""

TEN = """\
|  __    ___   |
| /_ |  / _ \  |
|  | | | | | | |
|  | | | | | | |
|  | | | |_| | |
|  |_|  \___/  |"""

NINE = """\
|   ___        |
|  / _ \       |
| | (_) |      |
|  \__, |      |
|    / /       |
|   /_/        |"""

EIGHT = """\
|   ___        |
|  / _ \       |
| | (_) |      |
|  > _ <       |
| | (_) |      |
|  \___/       |"""

SEVEN = """\
|  ______      |
| |____  |     |
|     / /      |
|    / /       |
|   / /        |
|  /_/         |"""

SIX = """\
|    __        |
|   / /        |
|  / /_        |
| | '_ \       |
| | (_) |      |
|  \___/       |"""

FIVE = """\
|  _____       |
| | ____|      |
| | |__        |
| |___ \       |
|  ___) |      |
| |____/       |"""

FOUR = """\
|  _  _        |
| | || |       |
| | || |_      |
| |__   _|     |
|    | |       |
|    |_|       |"""

THREE = """\
|  ____        |
| |___ \       |
|   __) |      |
|  |__ <       |
|  ___) |      |
| |____/       |"""

TWO = """\
|  ___         |
| |__ \        |
|    ) |       |
|   / /        |
|  / /_        |
| |____|       |"""

# BOUNDRY
# val  * 6
# suit * 5
# BOUNDRY
_CARD_HEIGHT = 13
_SUITS = (SPADE, CLUB, DIAMOND, HEART)
_VALS = (ACE, KING, QUEEN, JACK, TEN, NINE, EIGHT,
         SEVEN, SIX, FIVE, FOUR, THREE, TWO)

_SUIT_DICT = {Suit.CLUB:CLUB,Suit.DIAMOND:DIAMOND,Suit.HEART:HEART,Suit.SPADE:SPADE}


def make_const(val, suit):
    return f"{BOUNDRY}\n{val}\n{suit}\n{BOUNDRY}"


def print_const_list(cards):
    '''
    Prints a list of cards horizontally alligned
    ASSERT: cards is a list of string literals, each literal being the 
    full ASCII representation of a card, literals should have \n seperators 
    '''
    exploded = [card.splitlines() for card in cards]
    for i in range(_CARD_HEIGHT):
        for c in exploded:
            print(c[i], end="")
        print()


def main():
    deck = product(_SUITS, _VALS)
    deck2 = []
    for x in deck:
        deck2.append(make_const(x[1], x[0]))
    shuffle(deck2)
    prev = 0
    for i in range(5,52,5):
        print_const_list(deck2[prev:i])
        prev = i
    print_const_list(deck2[prev:])
        


if __name__ == '__main__':
    main()
