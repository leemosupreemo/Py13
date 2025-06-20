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
        obs_size = self.num_players * 13 + 52 + 1
        self.observation_space = spaces.Box(low=0, high=1, shape=(obs_size,), dtype=np.int8)
        self.action_space = spaces.Discrete(NUM_ACTIONS)

    def _encode_state(self):
        """Return a flat representation of the current game state."""
        # Placeholder encoding: zero vector
        return np.zeros(self.observation_space.shape, dtype=np.int8)

    def _apply_action(self, action: int):
        """Apply action to the underlying game engine.

        This is a stub implementation that should be extended with
        full game logic.
        """
        obs = self._encode_state()
        reward = 0.0
        done = False
        info = {}
        return obs, reward, done, info

    def reset(self):
        """Start a new game and return the initial observation."""
        self.game = Py13Game(self.num_players)
        return self._encode_state()

    def step(self, action: int):
        """Apply the given action and return the next state and reward."""
        obs, reward, done, info = self._apply_action(action)
        return obs, reward, done, info
