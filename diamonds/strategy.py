def calculate_average_opponent_bid(opponent_bids):
    if opponent_bids:
        return sum(opponent_bids) / len(opponent_bids)
    else:
        return 7  # Default average bid if no opponent bids are available


def select_bid_index(computer_hand, bid_index):
    return max(bid_index, -len(computer_hand))


def computer_bid(computer_hand, diamond_card, rounds_played, opponent_bids, computer_score, player_score):
    high_value_threshold = 10
    late_game_rounds = 4
    remaining_diamonds = 13 - rounds_played

    avg_opponent_bid = calculate_average_opponent_bid(opponent_bids)

    if remaining_diamonds <= late_game_rounds:
        bid_index = -1 if computer_score < player_score else -3
    else:
        if diamond_card > high_value_threshold:
            bid_index = -2
        else:
            bid_index = -3 if avg_opponent_bid < 7 else -4

    bid_index = select_bid_index(computer_hand, bid_index)
    bid = computer_hand.pop(bid_index)
    return bid
