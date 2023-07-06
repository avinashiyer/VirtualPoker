from itertools import filterfalse

import card_strings
import poker
from card_enums import Hands, Suit, Values
from deal import Deal
from os import get_terminal_size
from enum import Enum, auto


class Game():
    MULTIS = Hands.get_multis()
    STRINGS = Hands.get_strings()
    # Hard coded for now but child class could change hand sizes for different flavors of poker
    HAND_SIZE = 5
    CARD_WIDTH = len(card_strings.BOUNDRY)
    START = 0
    DEALT = 1
    TRADED = 2 
    
    
    def __init__(self) -> None:
        self.money = 100
        self.deck = poker.Deck()
        self.deal = Deal()
        self.state = Game.START

    def deal_hand(self):
        hand = [self.deck.pop() for _ in range(Game.HAND_SIZE)]
        self.deal.add_cards(hand)
        self.state = Game.DEALT

    def print_hand(self):
        print(self.deal)
        positions_string = []
        for pos in range(len(self.deal.deal)):
            number = f"({pos+1})"
            # creates a string of the form: "      (1)      "
            positions_string.append(f"{number:^{Game.CARD_WIDTH}}")
        print("".join(positions_string))
        if self.state==Game.DEALT:
            print(f'CURRENT HAND: {self.deal.hand}')
        elif self.state == Game.TRADED:
            self.print_result()
        else:
            print(f'Called print hand in invalid state. State: {self.state}')

    def print_result(self):
        print(f"END RESULT IS:\n{self.deal.hand:^{get_terminal_size()[0]}}")
    
    def trade_in(self, positions: list[int]):
        removed = self.deal.remove_cards(positions)
        self.deck.shuffle_deck()
        new_cards = [self.deck.pop() for _ in range(len(positions))]
        self.deal.add_cards(new_cards)
        self.deck.extend(removed)
        self.state = 2

    @staticmethod
    def validate_and_extract_input(input: str) -> list[int] | None:
        split = input.split()
        if not split:
            return None
        if len(split) == 1:
            word = split[0].lower()
            if any(word == sentinel for sentinel in ('quit', 'q', 'exit')):
                exit()
            elif any(word == sentinel for sentinel in ('help', 'h')):
                print("Input positions for trade in (space delimited) e.g. \'0 3 4\'")
                return None
        baddies = list(filterfalse(str.isnumeric, split))
        if len(baddies) > 0:
            s = ", ".join(baddies)
            print(f"\'{s}\' is/are invalid input")
            return None
        return [int(tok)-1 for tok in split]
    

    def reset(self):
        self.deck.extend(self.deal.deal)
        self.deal.deal.clear()
        self.deal.trade_pos.clear()
        self.state = 0


def ask_for_input():
    while True:
        try:
            inp = input("Enter positions for trade-in:")
        except EOFError:
            exit()
        pos = Game.validate_and_extract_input(inp)
        if pos:
            return pos

def main():
    g = Game()
    print("Welcome bubby :)")
    counter = 1
    while True:
        print(f'Round {counter}')
        g.deck.shuffle_deck()
        g.deal_hand()
        g.print_hand()
        pos = ask_for_input()
        g.trade_in(pos)
        g.print_hand()
        input("Press enter to start a new round")
        g.reset()
        counter += 1
        
