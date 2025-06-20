import random
from . import deck, player

class Py13Game:
    """Simple non-interactive game engine for Tiến Lên."""

    def __init__(self, num_players=4):
        self.num_players = num_players
        self.players = [player.Player(f"Player {i}") for i in range(num_players)]
        self.deck = deck.Deck()
        self.card_stack = []
        self.prev_move = 0
        self.num_passes = 0
        self.player_turn = None
        self.deal_cards()
        self.player_order()

    def deal_cards(self):
        for _ in range(13):
            for p in self.players:
                p.draw_card(self.deck)

    def player_order(self):
        self.player_turn = random.choice(self.players)

    def next_player(self):
        idx = self.players.index(self.player_turn)
        self.player_turn = self.players[(idx + 1) % self.num_players]
