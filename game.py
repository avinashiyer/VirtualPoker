from itertools import filterfalse

import card_strings
import poker
from card_enums import Hands, Suit, Values
from deal import Deal
from os import get_terminal_size


class Game:
    MULTIS = Hands.get_multis()
    STRINGS = Hands.get_strings()
    HAND_SIZE = 5
    CARD_WIDTH = len(card_strings.BOUNDRY)

    def __init__(self) -> None:
        self.money = 100
        self.deck = poker.Deck()
        self.deal = Deal()
        self.state = 0

    def deal_hand(self):
        hand = [self.deck.pop() for _ in range(Game.HAND_SIZE)]
        self.deal.add_cards(hand)
        self.state = 1
        self.print_hand()

    def print_hand(self):
        print(self.deal)
        positions_string = []
        for pos in range(len(self.deal.deal)):
            number = f"({pos+1})"
            positions_string.append(f"{number:^{Game.CARD_WIDTH}}")
        positions_string = "".join(positions_string)
        print(positions_string)
        flags = self.deal.search_hand()
        if self.state==1:
            print(f'CURRENT HAND: {Game.STRINGS[flags]}')
        elif self.state == 2:
            self.print_result()
        else:
            print(f'Called print hand in invalid state. State: {self.state}')

    def trade_in(self, positions: list[int]):
        removed = self.deal.remove_cards(positions)
        self.deck.extend(removed)
        self.deck.shuffle_deck()
        new_cards = [self.deck.pop() for _ in range(len(positions))]
        self.deal.add_cards(new_cards)
        self.state = 2
        self.print_hand()

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
    
    def print_result(self):
        flags = self.deal.search_hand()
        print(f"END RESULT IS:\n{self.STRINGS[flags]:^{get_terminal_size()[0]}}")

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
        pos = ask_for_input()
        g.trade_in(pos)
        input("Press enter to start a new round")
        g.reset()
        counter += 1
        
