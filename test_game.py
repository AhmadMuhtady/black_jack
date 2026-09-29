from game import calculate_score, determine_outcome, calculate_payout

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
    (10, 'bust', {}, -10),
    (10, 'loss', {}, -10),
    (10, 'push', {}, 0),
    (10, 'win', {}, 10.0),
    (10, 'blackjack', {}, 15.0),
    (10, 'blackjack', {'blackjack_payout': 1.2}, 12.0),
    (20, 'win', {'win_payout': 2.0}, 40.0),
]


if __name__ == "__main__":
    for hand, expected in test_hands:
        score = calculate_score(hand)
        assert score == expected, f"Score failed for {hand}: expected {expected}, got {score}"
    print("calculate_score: all tests passed!")


    for player, dealer, expected in outcome_tests:
        outcome = determine_outcome(player, dealer)
        assert outcome == expected, f"Outcome failed for player {player} vs dealer {dealer}: expected '{expected}', got '{outcome}'"
    print("determine_outcome: all tests passed!")


    for bet, outcome, extra_rules, expected in payout_tests:
        payout = calculate_payout(bet, outcome, **extra_rules)
        assert payout == expected, f"Payout failed for bet {bet}, outcome '{outcome}', kwargs {extra_rules}: expected {expected}, got {payout}"
    print("calculate_payout: all tests passed!")

    
    try:
        calculate_payout(10, 'win', invalid_key=99)
        raise AssertionError("calculate_payout failed to raise TypeError on invalid kwarg")
    except TypeError:
        pass
    print("calculate_payout invalid kwargs: test passed!")

    print("\nAll suites passed cleanly!")