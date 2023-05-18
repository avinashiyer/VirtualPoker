# Tests for basic functionality of core poker code
from timeit import timeit
import unittest
import poker as p
from VirtualPoker.card_enums import Values as v, Suit as s
from operator import attrgetter
from copy import deepcopy


class TestBase(unittest.TestCase):

        
    
    def val_and_suit_eq(first, second, msg):
        # unittest already checks types strictly
        if first != second or first.suit != second.suit:
            raise TestBase.failureException(
                f'{str(first)} unequal to {str(second)}')

    def setUp(self) -> None:
        self.addTypeEqualityFunc(p.Card, TestBase.val_and_suit_eq)
        return super().setUp()

    def test_sort_value_suit(self):
        original = p.Deck()
        expected = [p.Card(v.TWO,s.SPADE),
                    p.Card(v.THREE,s.SPADE),
                    p.Card(v.THREE,s.CLUB),
                    p.Card(v.FOUR,s.DIAMOND),
                    p.Card(v.EIGHT,s.HEART),
                    p.Card(v.EIGHT,s.DIAMOND),
                    p.Card(v.ACE,s.DIAMOND)
                    ]
        original.deck = [p.Card(x.value,x.suit) for x in expected]
        original.shuffle_deck()
        original.sort(key=attrgetter('value','suit')) 
        self.assertEqual(expected,original.deck)
        
    
    
    def test_deck_create(self):
        expected = [p.Card(val, suit) for val in v for suit in s]
        actual = p.Deck()
        self.assertEqual(len(actual.deck),52)
        expected.sort(key=attrgetter('value','suit'))
        actual.sort(key=attrgetter('value','suit'))
        for exp, act in zip(expected,actual):
            self.assertEqual(exp,act)
    
    # Has a ~1/(52!) chance of giving a false negative (shuffle returns original ordering)
    def test_shuffle(self):
        shuf = p.Deck()
        orig = deepcopy(shuf)
        shuf.shuffle_deck()
        self.assertNotEqual(shuf,orig)
    
    
    
    
        


if __name__ == '__main__':
    unittest.main()
