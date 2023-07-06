from collections import Counter

from card_enums import Hands, Suit, Values
from card_printer import stringify_card_list
from poker import Card


class Deal:
    '''
    Class that models a five card draw from the deck
    Implements searching for hands (e.g. two pair, full house)
    '''

    # Special case due to ace's duality as lowest|highest
    _low_straight = [
        Card(Values.ACE, Suit.SPADE),
        Card(Values.TWO, Suit.DIAMOND),
        Card(Values.THREE, Suit.HEART),
        Card(Values.FOUR, Suit.CLUB),
        Card(Values.FIVE, Suit.SPADE)
    ]
    _low_straight.sort()
    # Used for testing for royal flush
    _high_straight = [
        Card(Values.TEN, Suit.CLUB),
        Card(Values.JACK, Suit.DIAMOND),
        Card(Values.QUEEN, Suit.SPADE),
        Card(Values.KING, Suit.HEART),
        Card(Values.ACE, Suit.SPADE)
    ]

    def __init__(self, cards=[]):
        self.deal: list[Card | None] = cards
        self.trade_pos: list[int] = []
        self._hand = None

    @property
    def hand(self):
        """Hand that this deal Contains"""
        if self._hand is None:
            try:
                self._hand = self.search_hand()
            except (AssertionError,ValueError):
                return Hands.NOTHING
        return self._hand
            
    def __str__(self):
        return stringify_card_list(self.deal)
    
    def __repr__(self):
        return f"DEAL: {self.deal}\nTRADE_POS: {self.trade_pos}"
    
    def add_cards(self, to_add: list[Card]):
        '''
        'to_add' should be an iterable of Card objects, 
        (does not clone cards) 
        '''
        # Fill missing positions before appending to end
        for pos in self.trade_pos:
            self.deal[pos] = to_add.pop()
        self.deal.extend(to_add)
        self.trade_pos.clear()
        self._hand = None

    def remove_cards(self, positions: list[int]):
        '''
        Takes in a list of positions to remove from our deal, returns the Card 
        objects removed
        '''
        assert len(positions) <= len(self.deal)
        self.trade_pos = positions.copy()
        to_return = []
        for pos in positions:
            to_return.append(self.deal[pos])
            self.deal[pos] = None
        self._hand = None
        return to_return

    @staticmethod
    def pairs_search(pairs: Counter) -> Hands:
        assert pairs.total() == 5
        size = len(pairs)
        # Counter.most_common(1) returns singleton list with tuple, i.e. [(value,count),]
        _,most_common_count = pairs.most_common(1)[0]
        if size > 3:
            # only one pair return empty flag
            return Hands.NOTHING
        elif size == 3:
            # Size of 3 implies Two cases: [(x,x,x),y,z] or [(x,x),(y,y),z]
            if most_common_count == 3:
                return Hands.THREE_O_KIND
            else:
                return Hands.TWO_PAIR
        elif size == 2:
            # Size of two implies two cases: [(x,x,x,x),y] or [(x,x,x),(y,y)]
            if most_common_count == 4:
                return Hands.FOUR_O_KIND
            else:
                return Hands.FULL_HOUSE
        else:
            # Reachable only if passed in hand breaks assumption of 4 cards per value
            raise ValueError(f"Illegitimate hand passed to pairs_search\n{pairs}")
                

    @staticmethod
    def straight_search(sHand:list[Card]):
        '''
        Assumes passed list is sorted ascending by value
        '''
        
        #A hand is a straight iff when the lowest value is 4 ranks below
        # the highest. Proof: I made it up (Brute forced it)
        if sHand[0].value == sHand[-1].value-4:
            return Hands.STRAIGHT
        elif sHand == Deal._low_straight:
            return Hands.STRAIGHT
        else:
            return Hands.NOTHING

    @staticmethod
    def flush_search(hand):
        first_suit = hand[0].suit
        for c in hand[1:]:
            if c.suit != first_suit:
                return Hands.NOTHING
        return Hands.FLUSH

    @staticmethod
    def search_hand_static(deal:list[Card]):
        '''
        Takes in a list of cards and searches for hands within. 
        Seperated from instance method to remove overhead of 
        deal objects and checks when needed.
        '''
        pairs:Counter = Counter([c.value for c in deal])
        flags: Hands = Deal.pairs_search(pairs)
        if len(pairs) < 5:
            # Any pairs preclude other hands
            return flags
        sHand:list[Card] = sorted(deal)
        flags = Deal.straight_search(sHand)
        flags |= Deal.flush_search(sHand)
        if Hands.FLUSH in flags and Hands.STRAIGHT in flags:
            if sHand == Deal._high_straight:
                flags = Hands.ROYAL_FLUSH
            else:
                flags = Hands.STRAIGHT_FLUSH
        return flags
        
    
    
    
    def search_hand(self):
        '''
        Instance method of search hand that adds checks for assumptions.
        Better to use this one than the static method
        '''
        assert len(self.deal) == 5
        hand: list[Card] = [card for card in self.deal if card]
        if len(self.deal) != len(hand):
            raise ValueError("None value in list passed to search hand")
        return Deal.search_hand_static(hand)
