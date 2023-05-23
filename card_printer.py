import card_strings as card_string
from card_enums import Values,Suit


# Add 2 for top and bottom boundrys 
_VAL_HEIGHT = len(card_string.ACE)
_SUIT_HEIGHT = len(card_string.SPADE)
_CARD_HEIGHT = 1 + _VAL_HEIGHT + _SUIT_HEIGHT + 1

# Maps suit card_enums to string constants
_SUIT_TO_STRING = {Suit.CLUB: card_string.CLUB,
                   Suit.DIAMOND: card_string.DIAMOND,
                   Suit.HEART: card_string.HEART,
                   Suit.SPADE: card_string.SPADE}

# Maps val card_enums to string constants
_VAL_TO_STRING = {Values.TWO: card_string.TWO,
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
                  Values.ACE: card_string.ACE}


def make_const(val:Values, suit:Suit):
    '''
    Takes in val enum and suit enum and returns string constant representation
    of that card
    '''
    str_builder = [card_string.BOUNDRY]
    str_builder.extend(_VAL_TO_STRING[val])
    str_builder.extend(_SUIT_TO_STRING[suit])
    str_builder.append(card_string.BOUNDRY)
    return "\n".join(str_builder)


def stringify_card_list(cards):
    '''
    constructs a string of cards horizontally alligned
    
    ASSERT: cards is a list of (Value,Suit) tuples
    '''
    val_strings = [_VAL_TO_STRING[card[0]] for card in cards]
    suit_strings = [_SUIT_TO_STRING[card[1]] for card in cards]
    str_builder = [card_string.BOUNDRY * len(cards)]
    # Following for loops iterate add one horizontal line of the desired string
    # to string builder per iteration. Essentially an iteration of the transpose
    # of val_strings then suit_strings 
    for line in range(_VAL_HEIGHT):
        to_add = ""
        for val in val_strings:
            to_add += val[line]
        str_builder.append(to_add)
    for line in range(_SUIT_HEIGHT):
        to_add = ""
        for suit in suit_strings:
            to_add += suit[line]
        str_builder.append(to_add)
    str_builder.append(card_string.BOUNDRY * len(cards))
    return "\n".join(str_builder)
    

if __name__ == '__main__':
    from itertools import product
    deck = list(product(Values,Suit))
    prev = 0
    for i in range(0,len(deck),4):
        print(stringify_card_list(deck[prev:i]))
        prev = i
    print(stringify_card_list(deck[prev:]))