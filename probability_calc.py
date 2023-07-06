from poker import Deck
from card_enums import Values, Suit, Hands
from itertools import combinations
from game import Game
from deal import Deal

PAYOFFS = Hands.get_multis()

# Dict that maps k to all indexes an nChooseK would generate
# eg. 2 : [(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)]
COMBINATIONS = {k:(list(combinations(range(Game.HAND_SIZE),k))) \
     for k in range(1,Game.HAND_SIZE+1)}


def brute_force(deck:Deck,positions:tuple[int],hand:Deal):
     hand_copy = [card for card in hand.deal if card is not None]
     counter = 0
     ev_sum = 0.0
     for draw in combinations(deck,len(positions)):
          counter += 1
          for pos,card in zip(positions,draw):
               hand_copy[pos] = card
          flag = Deal.search_hand_static(hand_copy)
          ev_sum += PAYOFFS[flag]
     return ev_sum / counter

def calc_ev(deck:Deck,num_cards:int, deal:Deal):
     '''
     Calculate expected value given a deck and the number of cards we can draw,
     and remaining cards in our deal
     '''
     if num_cards == 0:
          return PAYOFFS[deal.hand]
     elif num_cards > Game.HAND_SIZE:
          raise ValueError(f'num_cards={num_cards} is too large for a hand size of {Game.HAND_SIZE}')
     positions_ev = {pos_tup : 0.0 for pos_tup in COMBINATIONS[num_cards]}
     pos_tups = list(positions_ev.keys())
     for pos_tup in pos_tups:
          positions_ev[pos_tup] = brute_force(deck,pos_tup,deal)
     return positions_ev