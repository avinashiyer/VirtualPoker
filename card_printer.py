from random import shuffle
import card_strings as card_string
from card_enums import Values, Suit
from poker import Card


_VAL_HEIGHT = len(card_string.ACE)
_SUIT_HEIGHT = len(card_string.SPADE)
# Add 2 for top and bottom boundrys
_CARD_HEIGHT = 1 + _VAL_HEIGHT + _SUIT_HEIGHT + 1

# Maps suit card_enums to string constants
_SUIT_TO_STRING = {
    Suit.CLUB: card_string.CLUB,
    Suit.DIAMOND: card_string.DIAMOND,
    Suit.HEART: card_string.HEART,
    Suit.SPADE: card_string.SPADE,
}

# Maps val card_enums to string constants
_VAL_TO_STRING = {
    Values.TWO: card_string.TWO,
    Values.THREE: card_string.THREE,
    Values.FOUR: card_string.FOUR,
    Values.FIVE: card_string.FIVE,
    Values.SIX: card_string.SIX,
    Values.SEVEN: card_string.SEVEN,
    Values.EIGHT: card_string.EIGHT,
    Values.NINE: card_string.NINE,
    Values.TEN: card_string.TEN,
    Values.JACK: card_string.JACK,
    Values.QUEEN: card_string.QUEEN,
    Values.KING: card_string.KING,
    Values.ACE: card_string.ACE,
}


def stringify_card(card: Card) -> str:
    """
    Convenience method to call make_const()
    """
    if not card:
        return '\n'.join(card_string.BACK)
    return make_const(card.value, card.suit)


def make_const(val: Values, suit: Suit) -> str:
    """
    Takes in val enum and suit enum and returns string constant representation
    of that card
    """
    str_builder = [card_string.BOUNDRY]
    str_builder.extend(_VAL_TO_STRING[val])
    str_builder.extend(_SUIT_TO_STRING[suit])
    str_builder.append(card_string.BOUNDRY)
    return "\n".join(str_builder)


def stringify_card_list(cards: list[Card|None]) -> str:
    """
    constructs a string of cards horizontally alligned

    ASSERT: type(cards[0]) is poker.Card
    """
    val_strings = [_VAL_TO_STRING[card.value]
                   if card else card_string.BACK_TOP for card in cards]
    suit_strings = [_SUIT_TO_STRING[card.suit]
                    if card else card_string.BACK_BOT for card in cards]
    str_builder = [card_string.BOUNDRY * len(cards)]
    # For loops iterate over transpose of val_strings and suit_strings and add
    # a 'row' at a time
    for line in range(_VAL_HEIGHT):
        to_add = []
        for val in val_strings:
            to_add.append(val[line])
        to_add = "".join(to_add)
        str_builder.append(to_add)
    for line in range(_SUIT_HEIGHT):
        to_add = []
        for suit in suit_strings:
            to_add += suit[line]
        to_add = "".join(to_add)
        str_builder.append(to_add)
    str_builder.append(card_string.BOUNDRY * len(cards))
    return "\n".join(str_builder)


if __name__ == "__main__":
    from itertools import product

    deck = list(product(Values, Suit))
    deck = [Card(val, suit) for val, suit in deck]
    prev = 0
    for i in range(0, len(deck), 4):
        print(stringify_card_list(deck[prev:i])) # type: ignore
        prev = i
    print(stringify_card_list(deck[prev:])) # type: ignore
    shuffle(deck)
    a = [deck[3], None, deck[26], None, deck[4], deck[5], deck[18], deck[11]]
    print(stringify_card_list(a))
