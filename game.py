import random

rules = """
Player actions: hit (take a card) or stand (stop). Doubling down is optional; leave it for the stretch goal.
Bust: over 21 loses right away. If the player busts, the dealer doesn't play that hand.
Natural blackjack: an Ace plus a 10-value card as your first two cards. It pays 3:2, while a normal win pays 1:1.
Push: a tie. The player gets their bet back.
Dealer: hit on 16 or less, stand on 17 or more. The dealer makes no decisions.

"""

BLACKJACK = 21
DEALER_STANDS_ON = 17
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':1}




def create_deck():
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
    has_ace = False

    for card in hand:
        card_value = values[card[0]]
        if card[0] == 'Ace':
           has_ace = True

        hand_score += card_value


    if has_ace and ((hand_score + 10) <= BLACKJACK):
        hand_score += 10

    return hand_score
    


def dealer_play(deck, current_hand):
    dealer_score = calculate_score(current_hand)

    while dealer_score < DEALER_STANDS_ON:
        new_card = deal_card(deck)
        current_hand.append(new_card)
        dealer_score = calculate_score(current_hand) 

    return dealer_score


def calculate_payout(bet_amount, outcome, **kwargs):
    allowed_keys = {'win_payout', 'blackjack_payout'}
    unexpected_keys = set(kwargs) - allowed_keys

    if unexpected_keys:
        raise TypeError(f"payout got unexpected Ratio Type: {', '.join(sorted(unexpected_keys))}")


    win_ratio = kwargs.get('win_payout',1.0)
    blackjack_ratio = kwargs.get('blackjack_payout',1.5)
   

    outcome = outcome.lower()

    if outcome in ('loss','bust'):
        return -bet_amount
    elif outcome == 'push':
        return 0
    elif outcome == 'win':
        return bet_amount * win_ratio
    elif outcome == 'blackjack':
        return bet_amount * blackjack_ratio
    else:
        raise ValueError(f'Unkown hand outcome {outcome}')


def is_natural(hand):
    if not isinstance(hand, list):
         raise TypeError("Hand must be a List")
    
    return len(hand) == 2 and calculate_score(hand) == BLACKJACK


def determine_outcome(player_hand, dealer_hand):
    if not (isinstance(player_hand, list) and isinstance(dealer_hand, list)):
        raise TypeError("Hands must be lists")
    
    is_player_nutral = is_natural(player_hand)
    is_dealer_nutral = is_natural(dealer_hand)

    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    if player_score > BLACKJACK:
        return 'bust'

    
    if is_player_nutral and is_dealer_nutral:
        return 'push'
    elif is_player_nutral:
        return 'blackjack'
    elif is_dealer_nutral:
        return 'loss'

    if dealer_score > BLACKJACK:
        return 'win'
    

    if player_score > dealer_score:
        return 'win'
    elif dealer_score > player_score:
        return 'loss'
    elif player_score == dealer_score:
        return 'push'

    

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
    deck = create_deck()
    random.shuffle(deck)
    card = deal_card(deck)