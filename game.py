import os
import random
import time

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


GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':1}
suit_symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Spades': '♠', 'Clubs': '♣'}
rank_short = {
    'Two': '2', 'Three': '3', 'Four': '4', 'Five': '5', 'Six': '6',
    'Seven': '7', 'Eight': '8', 'Nine': '9', 'Ten': '10',
    'Jack': 'J', 'Queen': 'Q', 'King': 'K', 'Ace': 'A'
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def format_card(card):
    rank, suit = card
    symbol = suit_symbols[suit]
    card_color = RED if suit in ('Hearts', 'Diamonds') else RESET
    return f"[{BOLD}{rank_short[rank]}{card_color}{symbol}{RESET}]"


def display_hand(hand):
    return " ".join(format_card(c) for c in hand)




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
        time.sleep(1.0)
        new_card = deal_card(deck)
        current_hand.append(new_card)
        dealer_score = calculate_score(current_hand)
        print(f"Dealer hits: {format_card(new_card)} | Hand: {display_hand(current_hand)} (Score: {dealer_score})")

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
    
    is_player_natural = is_natural(player_hand)
    is_dealer_natural = is_natural(dealer_hand)

    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    if player_score > BLACKJACK:
        return 'bust'
    
    if is_player_natural and is_dealer_natural:
        return 'push'
    elif is_player_natural:
        return 'blackjack'
    elif is_dealer_natural:
        return 'loss'

    if dealer_score > BLACKJACK:
        return 'win'

    if player_score > dealer_score:
        return 'win'
    elif dealer_score > player_score:
        return 'loss'
    else:
        return 'push'

    


def prompt_int(prompt_message, error_message):
    while True:
        raw_val = input(prompt_message).strip()

        try:
            val = int(raw_val)
        except ValueError:
            print(f"{RED}Invalid input. Please enter a whole number.{RESET}")
            continue

        if val < MIN_BET:
            print(f"{RED}{error_message}{RESET}")
            continue

        return val


def get_bankroll():
    bankroll = prompt_int(
        "Please Deposit money to play: ",
        f"Deposit amount should be Higher or equal to {MIN_BET:.2f}"
    )
    print(f"{GREEN}${bankroll:.2f} has been deposited successfully!{RESET}\n")
    return bankroll


def get_bet(bankroll):
    if bankroll < MIN_BET:
        raise ValueError(f"Cannot place a bet with a bankroll of {bankroll}.")

    while True:
        bet = prompt_int(
            f"Current bankroll: {BOLD}${bankroll:.2f}{RESET}. Enter your bet: $",
            f"Bet should be Higher or equal to {MIN_BET:.2f}"
        )

        if bet > bankroll:
            print(f"{RED}You cannot bet more than your bankroll (${bankroll:.2f}).{RESET}")
            continue

        return bet


def prompt_choice(prompt_message, action_map):
    while True:
        user_input = input(prompt_message)
        cleaned_input = user_input.strip().lower()

        if cleaned_input not in action_map:
            valid_options = "/".join(sorted(set(action_map.values())))
            print(f"{RED}Invalid input '{user_input}'. Please choose: {valid_options}{RESET}")
            continue

        return action_map[cleaned_input]


def get_action():
    return prompt_choice(
        f"{YELLOW}Do you want to [H]it or [S]tand?: {RESET}",
        {"h": "hit", "hit": "hit", "s": "stand", "stand": "stand"}
    )


def get_another_round():
    return prompt_choice(
        f"{YELLOW}Do you want to play another round [Y]ES or [N]O?: {RESET}",
        {"y": "yes", "yes": "yes", "n": "no", "no": "no"}
    )

# In player_turn():
def player_turn(deck, hand):
    score = calculate_score(hand)

    while score < BLACKJACK:
        print(f"\nYour hand: {display_hand(hand)} | Score: {score}")

        action = get_action()

        if action == 'hit':
            card = deal_card(deck)
            hand.append(card)
            print(f"You drew: {format_card(card)}")
            
            score = calculate_score(hand)
            print(f"Your hand: {display_hand(hand)} | Score: {score}")
            if score > BLACKJACK:
                print(f"{RED}Busted with {score}!{RESET}")
                break
            elif score == BLACKJACK:
                print(f"{GREEN}21! Standing automatically.{RESET}")
                break
        else:
            print(f"You chose to stand at {score}.")
            break
    return score


def play_round(deck, bankroll,round_number):
    print(f"\n{CYAN}{'='*15} ROUND {round_number} {'='*15}{RESET}")
    bet = get_bet(bankroll)

    player_hand = [deal_card(deck) for _ in range(2)]
    dealer_hand = [deal_card(deck) for _ in range(2)]
    print(f"\nYour hand:   {display_hand(player_hand)} | Score: {calculate_score(player_hand)}")
    print(f"Dealer shows: {format_card(dealer_hand[0])} [?]")

    if is_natural(player_hand) or is_natural(dealer_hand):
            print(f"\nDealer reveals hole card: {format_card(dealer_hand[1])}")
            print(f"Dealer hand:  {display_hand(dealer_hand)} | Score: {calculate_score(dealer_hand)}")
    else:
        player_score = player_turn(deck, player_hand)
        
        

        if player_score <= BLACKJACK:
            print(f"\nDealer reveals hole card: {format_card(dealer_hand[1])}")
            dealer_play(deck, dealer_hand)
            print(f"Dealer finishes with: {display_hand(dealer_hand)} | Score: {calculate_score(dealer_hand)}")

    
    outcome = determine_outcome(player_hand, dealer_hand)
    
    payout = calculate_payout(bet,outcome)
    bankroll += payout
    if outcome in ('win', 'blackjack'):
        color = GREEN
    elif outcome == 'push':
        color = YELLOW
    else:
        color = RED

    print(f"\n{color}{BOLD}Round Result: {outcome.upper()}!{RESET}")
    print(f"Net change: {color}{'+' if payout > 0 else ''}{payout:.2f}{RESET}")
    print(f"Current Bankroll: {BOLD}${bankroll:.2f}{RESET}\n")

    return bankroll



def game():
    clear_screen()
    print(f"{BOLD}=== WELCOME TO BLACKJACK ==={RESET}\n")
    bankroll = get_bankroll()
    round_number = 1

    # Keep a running shoe across rounds
    deck = create_deck()
    random.shuffle(deck)

    while True:
        # Reshuffle if shoe gets low (< 15 cards)
        if len(deck) < 15:
            print(f"{YELLOW}[Reshuffling deck...]{RESET}")
            deck = create_deck()
            random.shuffle(deck)

        bankroll = play_round(deck, bankroll, round_number)

        if bankroll < MIN_BET:
            print(f"{RED}Bankroll is ${bankroll:.2f}. You ran out of money!{RESET}")
            break

        player_action = get_another_round()
        
        if player_action == 'yes':
            round_number += 1
            clear_screen()
            continue
        else:
            print(f"\n{BOLD}Cashing out with ${bankroll:.2f}. Thanks for playing!{RESET}")
            break
        


if __name__ == "__main__":
    game()

    