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
MIN_BET = 1
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

    

def get_bet(bankroll):
    if bankroll <= 0:
       raise ValueError(f"Cannot place a bet with a bankroll of {bankroll}.")
    while True:
        user_bet = input(f"Current bankroll: ${bankroll}. Enter your bet: ").strip()

        try:
            bet = int(user_bet)
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            continue

        if bet < MIN_BET:
            print('Bet should be Higher or equal to {MIN_BET}')
        elif bet > bankroll:
            print(f"You cannot bet more than your bankroll (${bankroll}).")
        else:
            return bet


def get_action():
    action_map = {
        'h': 'hit',
        'hit': 'hit',
        's': 'stand',
        'stand': 'stand'
        }

    while True:
        user_input = input("Do you want to [H]it or [S]tand?: ")

        user_action = user_input.strip().lower()

        if user_action not in action_map:
            print(f'Please Enter [H]it or [S]tand: your previous input {user_input}')
            continue
        
        
        return action_map[user_action]

test_hands = [
    ([('Five', 'Hearts'), ('Nine', 'Clubs')], 14),
    ([('King', 'Hearts'), ('Queen', 'Clubs')], 20),
    ([('Ace', 'Spades'), ('King', 'Hearts')], 21),
    ([('Ace', 'Spades'), ('Six', 'Hearts')], 17),
    ([('Ace', 'Spades'), ('Five', 'Hearts'), ('King', 'Clubs')], 16),
    ([('Ace', 'Spades'), ('Ace', 'Hearts')], 12),
    ([('Ace', 'Spades'), ('Ace', 'Hearts'), ('Nine', 'Clubs')], 21),
    ([('Ace', 'Spades'), ('Ace', 'Hearts'), ('Ace', 'Clubs'), ('Ace', 'Diamonds')], 14),
    ([('King', 'Hearts'), ('Queen', 'Clubs'), ('Five', 'Spades')], 25),
    ([('Ace', 'Spades'), ('King', 'Hearts'), ('Queen', 'Clubs')], 21),
    ([], 0),
]

outcome_tests = [
    ([('King', 'Hearts'), ('Queen', 'Clubs'), ('Five', 'Spades')], [('Ten', 'Hearts'), ('Nine', 'Clubs')], 'bust'),
    ([('Ace', 'Spades'), ('King', 'Hearts')], [('Ten', 'Clubs'), ('Five', 'Hearts'), ('Six', 'Spades')], 'blackjack'),
    ([('Ace', 'Spades'), ('King', 'Hearts')], [('Ace', 'Clubs'), ('Queen', 'Diamonds')], 'push'),
    ([('Ten', 'Hearts'), ('Five', 'Clubs'), ('Six', 'Spades')], [('Ace', 'Hearts'), ('King', 'Clubs')], 'loss'),
    ([('Ten', 'Hearts'), ('Eight', 'Clubs')], [('Ten', 'Spades'), ('Six', 'Hearts'), ('Seven', 'Clubs')], 'win'),
    ([('Ten', 'Hearts'), ('Eight', 'Clubs')], [('Ten', 'Spades'), ('King', 'Hearts')], 'loss'),
    ([('Ten', 'Hearts'), ('Nine', 'Clubs')], [('King', 'Spades'), ('Nine', 'Hearts')], 'push'),
    ([('Ten', 'Hearts'), ('Nine', 'Clubs')], [('King', 'Spades'), ('Eight', 'Hearts')], 'win'),
]

payout_tests = [
    # (bet, outcome, kwargs, expected_net)
    (10, 'bust', {}, -10),
    (10, 'loss', {}, -10),
    (10, 'push', {}, 0),
    (10, 'win', {}, 10.0),
    (10, 'blackjack', {}, 15.0),
    (10, 'blackjack', {'blackjack_payout': 1.2}, 12.0),
    (20, 'win', {'win_payout': 2.0}, 40.0),
]


if __name__ == "__main__":
    # 1. Test calculate_score
    for hand, expected in test_hands:
        score = calculate_score(hand)
        assert score == expected, f"Score failed for {hand}: expected {expected}, got {score}"
    print("calculate_score: all tests passed!")

    # 2. Test determine_outcome
    for player, dealer, expected in outcome_tests:
        outcome = determine_outcome(player, dealer)
        assert outcome == expected, f"Outcome failed for player {player} vs dealer {dealer}: expected '{expected}', got '{outcome}'"
    print("determine_outcome: all tests passed!")

    # 3. Test calculate_payout
    for bet, outcome, extra_rules, expected in payout_tests:
        payout = calculate_payout(bet, outcome, **extra_rules)
        assert payout == expected, f"Payout failed for bet {bet}, outcome '{outcome}', kwargs {extra_rules}: expected {expected}, got {payout}"
    print("calculate_payout: all tests passed!")

    # 4. Negative test: verify calculate_payout raises TypeError on unexpected kwargs
    try:
        calculate_payout(10, 'win', invalid_key=99)
        raise AssertionError("calculate_payout failed to raise TypeError on invalid kwarg")
    except TypeError:
        pass
    print("calculate_payout invalid kwargs: test passed!")

    print("\nAll suites passed cleanly!")