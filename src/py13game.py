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

    # New helper methods for simplified gameplay used by the
    # reinforcement-learning environment.  These do not implement the
    # full game logic but provide enough mechanics so that the
    # environment can terminate.

    def play_card(self, card_index: int) -> bool:
        """Play the card at ``card_index`` for the current player.

        Returns ``True`` if a card was successfully played, ``False`` if the
        index was invalid and the player effectively passed their turn.
        """
        hand = self.player_turn.hand
        if 0 <= card_index < len(hand):
            card = hand.pop(card_index)
            # For the stub engine we simply replace the stack with the card
            # played.  Detailed validation of moves is outside the scope of
            # this minimal implementation.
            self.card_stack = [card]
            self.num_passes = 0
            self.prev_move = 1
            self.next_player()
            return True

        # Invalid move counts as a pass.
        self.pass_turn()
        return False

    def pass_turn(self):
        """Current player chooses to pass."""
        self.num_passes += 1
        self.prev_move = 0
        if self.num_passes >= self.num_players - 1:
            # Everyone passed, reset the board
            self.card_stack = []
            self.num_passes = 0
        self.next_player()

    def is_game_over(self) -> bool:
        """Return ``True`` if any player has emptied their hand."""
        return any(p.num_cards() == 0 for p in self.players)
