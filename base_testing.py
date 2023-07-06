# Tests for basic functionality of core poker code
import unittest
from copy import deepcopy
from itertools import cycle
from operator import attrgetter
from random import shuffle
from timeit import timeit

from card_enums import Hands, Suit, Values
from deal import Deal
from poker import Card, Deck


def val_and_suit_eq(first, second, msg):
    '''
    Custom Card.__eq__ method to test val and suit 
    '''
    # unittest module already checks types strictly
    if first != second or first.suit != second.suit:  # type: ignore
        raise TestBase.failureException(
            f'{str(first)} unequal to {str(second)}')


class TestBase(unittest.TestCase):
    def setUp(self) -> None:
        self.addTypeEqualityFunc(Card, val_and_suit_eq)
        return super().setUp()

    @unittest.expectedFailure
    def test_custom_eq(self):
        first = Card(Values.ACE, Suit.SPADE)
        second = Card(Values.ACE, Suit.DIAMOND)
        self.assertEqual(first, second)

    def test_sort_value_suit(self):
        original = Deck()
        expected = [Card(Values.TWO, Suit.SPADE),
                    Card(Values.THREE, Suit.SPADE),
                    Card(Values.THREE, Suit.CLUB),
                    Card(Values.FOUR, Suit.DIAMOND),
                    Card(Values.EIGHT, Suit.HEART),
                    Card(Values.EIGHT, Suit.DIAMOND),
                    Card(Values.ACE, Suit.DIAMOND)
                    ]
        other_deck = Deck()
        other_deck.deck = expected
        original.deck = [Card(x.value, x.suit) for x in expected]
        original.shuffle_deck()
        self.assertNotEqual(original, other_deck)
        original.sort(key=attrgetter('value', 'suit'))
        self.assertEqual(other_deck, original.deck)

    def test_deck_create(self):
        expected = [Card(val, suit) for val in Values for suit in Suit]
        actual = Deck()
        self.assertEqual(len(actual.deck), 52)
        expected.sort(key=attrgetter('value', 'suit'))
        actual.sort(key=attrgetter('value', 'suit'))
        for exp, act in zip(expected, actual):
            self.assertEqual(exp, act)

    # Has a ~1/(52!) chance of giving a false negative (if shuffle returns original ordering)
    def test_shuffle(self):
        shuf = Deck()
        orig = deepcopy(shuf)
        shuf.shuffle_deck()
        self.assertNotEqual(shuf, orig)

    def test_low_straight_direct(self):
        deal = [
            Card(Values.ACE, Suit.CLUB),
            Card(Values.FIVE, Suit.SPADE),
            Card(Values.THREE, Suit.HEART),
            Card(Values.TWO, Suit.CLUB),
            Card(Values.FOUR, Suit.DIAMOND)
        ]
        deal.sort()
        flags = Deal.straight_search(deal)
        self.assertEqual(flags, Hands.STRAIGHT)

    def test_low_straight(self):
        cards = [
            Card(Values.ACE, Suit.SPADE),
            Card(Values.FIVE, Suit.SPADE),
            Card(Values.THREE, Suit.DIAMOND),
            Card(Values.TWO, Suit.HEART),
            Card(Values.FOUR, Suit.CLUB)
        ]
        shuffle(cards)
        d = Deal(cards)
        flags = d.search_hand()
        self.assertEqual(flags, Hands.STRAIGHT)

    def test_straight_direct(self):
        cards = [
            Card(6, 1),
            Card(7, 3),
            Card(8, 2),
            Card(9, 4),
            Card(10, 2)
        ]
        cards.sort()
        flags = Deal.straight_search(cards)
        self.assertEqual(flags, Hands.STRAIGHT)

    def test_straight(self):
        cards = [
            Card(6, 1),
            Card(7, 3),
            Card(8, 2),
            Card(9, 2),
            Card(10, 2)
        ]
        shuffle(cards)
        d = Deal(cards)
        flags = d.search_hand()
        self.assertEqual(flags, Hands.STRAIGHT)

    def test_high_straight(self):
        cards = [
            Card(10, 2),
            Card(13, 4),
            Card(14, 1),
            Card(11, 1),
            Card(12, 3)
        ]
        shuffle(cards)
        d = Deal(cards)
        flags = d.search_hand()
        self.assertEqual(flags, Hands.STRAIGHT)

    def test_low_straight_flush(self):
        cards = [Card(val, Suit.SPADE) for val in range(2, 6)]
        cards.append(Card(14, Suit.SPADE))
        shuffle(cards)
        d = Deal(cards)
        flags = d.search_hand()
        self.assertEqual(flags, Hands.STRAIGHT_FLUSH)

    def test_straight_flush(self):
        cards = [Card(val, Suit.DIAMOND) for val in range(8, 13)]
        shuffle(cards)
        d = Deal(cards)
        flags = d.search_hand()
        self.assertEqual(flags, Hands.STRAIGHT_FLUSH)

    def test_royal_flush(self):
        cards = [Card(val, Suit.HEART) for val in range(10, 15)]
        d = Deal(cards)
        self.assertEqual(d.search_hand(), Hands.ROYAL_FLUSH)

    def test_flush_direct(self):
        cards = [Card(val,2) for val in range(5,14,2)]
        flags = Deal.flush_search(cards)
        self.assertEqual(flags,Hands.FLUSH)
    
    def test_flush(self):
        cards = [Card(val,4) for val in range(2,15,3)]
        d = Deal(cards)
        self.assertEqual(d.search_hand(),Hands.FLUSH)
        
    def test_no_hand(self):
        cards = [
            Card(2, 2),
            Card(5, 2),
            Card(5, 2),
            Card(14, 2),
            Card(3, 1)
        ]
        shuffle(cards)
        d = Deal(cards)
        self.assertEqual(d.search_hand(), Hands.NOTHING)

    def test_no_hand_2(self):
        suits = cycle(Suit)
        vals = range(2,11,2)
        cards = [Card(val,st) for val,st in zip(vals,suits)]
        shuffle(cards)
        d = Deal(cards)
        self.assertEqual(d.search_hand(), Hands.NOTHING)
    
    def test_three_of_a_kind(self):
        cards = [
            Card(2,1),
            Card(3,4),
            Card(14,4),
            Card(14,1),
            Card(14,2)
        ]
        shuffle(cards)
        d = Deal(cards)
        self.assertEqual(d.search_hand(),Hands.THREE_O_KIND)
    
    def test_two_pair(self):
        cards = [
            Card(4,1),
            Card(14,1),
            Card(14,2),
            Card(8,1),
            Card(8,2)
        ]
        shuffle(cards)
        d = Deal(cards)
        self.assertEqual(d.search_hand(),Hands.TWO_PAIR)
    
    def test_four_of_a_kind(self):
        cards = [Card(4,st) for st in Suit]
        cards.append(Card(7,4))
        d = Deal(cards)
        self.assertEqual(d.search_hand(),Hands.FOUR_O_KIND)
    
    def test_full_house(self):
        cards = [
            Card(5,1),
            Card(5,4),
            Card(9,3),
            Card(9,2),
            Card(9,1)
        ]
        d = Deal(cards)
        self.assertEqual(d.search_hand(),Hands.FULL_HOUSE)

if __name__ == '__main__':
    unittest.main()
