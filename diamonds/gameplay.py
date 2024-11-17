import random
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = list(range(2, 15))  # Cards in hand initially

    def make_bid(self, bid):
        if bid in self.hand:
            self.hand.remove(bid)
            return bid
        else:
            raise ValueError("Invalid bid. You don't have that card.")

class Game:
    def __init__(self, player_name):
        self.player = Player(player_name)
        self.computer = Player("Computer")
        self.diamonds = list(range(2, 15))
        random.shuffle(self.diamonds)  # Shuffle diamond cards once
        self.player_score = 0
        self.computer_score = 0
        self.opponent_bids = []

    def score_round(self, diamond_card, player_bid, computer_bid):
        if player_bid > computer_bid:
            player_points = diamond_card
            computer_points = 0
        elif computer_bid > player_bid:
            player_points = 0
            computer_points = diamond_card
        else:  # Tie
            player_points = diamond_card / 2
            computer_points = diamond_card / 2

        return player_points, computer_points

    def play_round(self, player_bid_value):
        round_number = len(self.opponent_bids) + 1
        diamond_card = self.diamonds.pop(0)  # Pop the first diamond card
        computer_bid_value = computer_bid(
            self.computer.hand,
            diamond_card,
            round_number,
            self.opponent_bids,
            self.computer_score,
            self.player_score
        )
        self.opponent_bids.append(player_bid_value)

        self.score_round(diamond_card, player_bid_value, computer_bid_value)

    def determine_winner(self):
        if self.player_score > self.computer_score:
            return "You win!"
        elif self.computer_score > self.player_score:
            return "Computer wins!"
        else:
            return "It's a tie!"