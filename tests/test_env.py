import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.tienlen_env import TienLenEnv


def test_env_terminates():
    env = TienLenEnv(num_players=4)
    obs = env.reset()
    done = False
    steps = 0
    while not done and steps < 200:
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        steps += 1
    assert done, "Environment did not terminate within 200 steps"
