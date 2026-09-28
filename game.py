import random

rules = """
Player actions: hit (take a card) or stand (stop). Doubling down is optional; leave it for the stretch goal.
Bust: over 21 loses right away. If the player busts, the dealer doesn't play that hand.
Natural blackjack: an Ace plus a 10-value card as your first two cards. It pays 3:2, while a normal win pays 1:1.
Push: a tie. The player gets their bet back.
Dealer: your rule is right: hit on 16 or less, stand on 17 or more. The dealer makes no decisions.

"""


suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':1}




def creat_deck():
    deck = set([(y,x) for y in ranks for x in suits])
    if len(deck) != 52:
        raise ValueError(f"Deck must have 52 cards, got {len(deck)} cards")

    return list(deck)






def deal_card(deck):
    if not isinstance(deck,list):
        raise TypeError("Deck must be a List")
    
    card = deck.pop()
    return card


def calculate_score(hand):
    if not isinstance(hand,list):
        raise TypeError("Hand must be a List")   

    hand_score = 0
    BLACKJACK = 21
    has_ace = False

    for card in hand:
        card_value = values[card[0]]
        if 'Ace' in card:
           has_ace = True

        hand_score += card_value


    if has_ace and ((hand_score + 10) <= BLACKJACK):
        hand_score += 10

    return hand_score
    








test_hands = [
    ([('Five', 'Hearts'), ('Nine', 'Clubs')], 14),                                   # no Ace
    ([('King', 'Hearts'), ('Queen', 'Clubs')], 20),                                  # face cards
    ([('Ace', 'Spades'), ('King', 'Hearts')], 21),                                   # natural blackjack
    ([('Ace', 'Spades'), ('Six', 'Hearts')], 17),                                    # soft 17
    ([('Ace', 'Spades'), ('Five', 'Hearts'), ('King', 'Clubs')], 16),                # Ace must drop to 1
    ([('Ace', 'Spades'), ('Ace', 'Hearts')], 12),                                    # two Aces
    ([('Ace', 'Spades'), ('Ace', 'Hearts'), ('Nine', 'Clubs')], 21),                 # two Aces, one as 11
    ([('Ace', 'Spades'), ('Ace', 'Hearts'), ('Ace', 'Clubs'), ('Ace', 'Diamonds')], 14),  # four Aces
    ([('King', 'Hearts'), ('Queen', 'Clubs'), ('Five', 'Spades')], 25),              # bust, no Ace
    ([('Ace', 'Spades'), ('King', 'Hearts'), ('Queen', 'Clubs')], 21),               # Ace saves it as 1
    ([], 0),                                                                         # empty hand
]

if __name__ == "__main__":
    deck = creat_deck()
    random.shuffle(deck)
    card = deal_card(deck)
    print(card)

