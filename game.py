rules = """
Player actions: hit (take a card) or stand (stop). Doubling down is optional; leave it for the stretch goal.
Bust: over 21 loses right away. If the player busts, the dealer doesn't play that hand.
Natural blackjack: an Ace plus a 10-value card as your first two cards. It pays 3:2, while a normal win pays 1:1.
Push: a tie. The player gets their bet back.
Dealer: your rule is right: hit on 16 or less, stand on 17 or more. The dealer makes no decisions.

"""


suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':11, 'Queen':12, 'King':13, 'Ace':14}




def creat_deck():
    deck = [(y,x) for y in ranks for x in suits]
    return deck


