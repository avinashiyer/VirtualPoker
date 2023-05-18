from collections import Counter
from copy import deepcopy
from functools import total_ordering
from itertools import product
from random import shuffle
from typing import Iterable, List, Tuple
from poker import Card, Deck
from VirtualPoker.card_enums import Hands, Suit, Values


class Draw:
    '''
    Class that models a five card draw from the deck
    Keeps track of possible hands and counts
    '''
    
    def __init__(self, cards=[]):
        self.sorted = sorted(cards)
        self.positions = {pos:card for pos,card in enumerate(cards)}
        self.counter = Counter(x.value for x in cards)
        self.flags = Hands(0)
        self.trade_pos = []
    
    def add_cards(self,to_add:list):
        '''
        'to_add' should be an iterable of Card objects, 
        (does not clone cards) 
        '''
        self.sorted.extend(to_add)
        self.sorted.sort()
        self.counter.update(x.value for x in to_add)
        for pos,card in zip(self.trade_pos,to_add):
            self.positions[pos] = card
        self.trade_pos.clear()
        
    def remove_cards(self, positions:list):
        self.trade_pos = positions.copy()
        to_remove = [self.positions[pos] for pos in positions]
        
        
    @staticmethod
    def pairs_search(pairs: Counter):
        assert pairs.total() == 5
        size = len(pairs)
        if size > 3:
            # only one pair return empty flag
            return Hands(0)
        elif size == 3:
            if pairs[0] == 3:
                return Hands.THREE_O_KIND
            else:
                return Hands.TWO_PAIR
        else:
            return Hands.FOUR_O_KIND

    @staticmethod
    def straight_search(sHand):
        if sHand[0].value == sHand[-1].value-4:
            return Hands.STRAIGHT
        elif sHand == Deck._low_straight:
            return Hands.STRAIGHT
        else:
            return 0

    @staticmethod
    def flush_search(sHand):
        first_suit = sHand[0].suit
        for c in sHand[1:]:
            if c.suit == first_suit:
                return 0
        return Hands.FLUSH

    def search_hand(self):
        assert len(self.cards) == 5

        sHand = sorted(hand)
        pairs = Counter([c.value for c in hand])

        if len(pairs) == len(hand):
            # Unique values only
            flags = Deck.straight_search(sHand)
            flags |= Deck.flush_search(sHand)

            if Hands.STRAIGHT in flags and Hands.FLUSH in flags:
                if sHand == Deck._high_straight:
                    flags = Hands.ROYAL_FLUSH
                else:
                    flags = Hands.STRAIGHT_FLUSH
            return flags
        else:
            return Deck.pairs_search(pairs)