import numpy as np
import gym
from gym import spaces

from .py13game import Py13Game

NUM_ACTIONS = 53  # 52 cards + pass

class TienLenEnv(gym.Env):
    """Gym wrapper for the Py13 card game."""

    metadata = {"render.modes": ["human"]}

    def __init__(self, num_players: int = 4):
        super().__init__()
        self.num_players = num_players
        self.game = None
        self.steps = 0
        self.max_steps = 200
        obs_size = self.num_players * 13 + 52 + 1
        self.observation_space = spaces.Box(low=0, high=1, shape=(obs_size,), dtype=np.int8)
        self.action_space = spaces.Discrete(NUM_ACTIONS)

    def _encode_state(self):
        """Return a flat representation of the current game state."""
        # Placeholder encoding: zero vector
        state = np.zeros(self.observation_space.shape, dtype=np.int8)
        if self.game is None:
            return state

        # Encode the number of cards each player holds in a very simple form.
        # Each player gets a block of 13 values where the first ``n`` entries are
        # set to ``1`` if the player has ``n`` cards remaining.  This encoding is
        # extremely coarse but sufficient for testing purposes.
        for idx, p in enumerate(self.game.players):
            start = idx * 13
            state[start:start + p.num_cards()] = 1

        # The next 52 entries are a one-hot representation of the top card on
        # the stack if one exists.  Cards are identified by their position in
        # the deck (0-51).  Since ``deck.Card`` does not expose an index, we
        # synthesise one based on suit and value to keep things deterministic.
        if self.game.card_stack:
            card = self.game.card_stack[-1]
            suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
            suit_offset = suits.index(card.suit) * 13
            value_offset = card.value - 1
            state[self.num_players * 13 + suit_offset + value_offset] = 1

        # Final element indicates which player's turn it is.
        current = self.game.players.index(self.game.player_turn)
        state[-1] = current
        return state

    def _apply_action(self, action: int):
        """Apply action to the underlying game engine."""

        if self.game is None:
            raise ValueError("Environment must be reset before calling step().")

        if action == NUM_ACTIONS - 1:
            self.game.pass_turn()
        else:
            hand_size = self.game.player_turn.num_cards()
            if hand_size > 0:
                index = action % hand_size
                self.game.play_card(index)
            else:
                self.game.pass_turn()

        done = self.game.is_game_over()
        reward = 1.0 if done else 0.0
        obs = self._encode_state()
        info = {}
        return obs, reward, done, info

    def reset(self):
        """Start a new game and return the initial observation."""
        self.game = Py13Game(self.num_players)
        self.steps = 0
        return self._encode_state()

    def step(self, action: int):
        """Apply the given action and return the next state and reward."""
        obs, reward, done, info = self._apply_action(action)
        self.steps += 1
        if self.steps >= self.max_steps:
            done = True
        return obs, reward, done, info
