# One off script for converting specifically formatted ascii art into list declarations of the same art  

from card_enums import Values,Suit

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

# Maps suit card_enums to string constants
_SUIT_TO_STRING = {Suit.CLUB: CLUB,
                   Suit.DIAMOND: DIAMOND,
                   Suit.HEART: HEART,
                   Suit.SPADE: SPADE}

# Maps val card_enums to string constants
_VAL_TO_STRING = {Values.TWO: TWO,
                  Values.THREE: THREE,
                  Values.FOUR: FOUR,
                  Values.FIVE: FIVE,
                  Values.SIX: SIX,
                  Values.SEVEN: SEVEN,
                  Values.EIGHT: EIGHT,
                  Values.NINE: NINE,
                  Values.TEN: TEN,
                  Values.JACK: JACK,
                  Values.QUEEN: QUEEN,
                  Values.KING: KING,
                  Values.ACE: ACE}


def pretty_repr(ls,f):
    f.write('[\n')
    for s in ls:
        f.write('\t\'')
        f.write(s)
        f.write('\',\n')
    f.write(']\n')

f = open("scratch.txt","wt+")
f.write("------------VALS-----------\n\n")
for k,v in _VAL_TO_STRING.items():
    f.write(k.name)
    f.write(' = ')
    pretty_repr(v.splitlines(), f)
    f.write('\n')

f.write("------------SUITS-------------\n\n")
for k,v in _SUIT_TO_STRING.items():
    f.write(k.name)
    f.write(" = ")
    pretty_repr(v.splitlines(), f)
    f.write("\n")
f.close()    