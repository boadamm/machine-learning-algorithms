from dataclasses import dataclass
from typing import List

import numpy as np

from .env import ACTION_SPACE, GridWorld


@dataclass
class QLearningHyperparameters:
    alpha: float = 0.1
    gamma: float = 0.9
    epsilon: float = 0.1
    episodes: int = 5000


def q_learning(
    env: GridWorld,
    params: QLearningHyperparameters = QLearningHyperparameters(),
    log_returns: bool = False,
) -> np.ndarray:
    """Perform tabular Q-learning to find the optimal Q-function.

    Args:
        env (GridWorld): The environment to learn from.
        params (QLearningHyperparameters, optional):
            Hyperparameters for Q-learning.
            Defaults to `QLearningHyperparameters()`.
        log_returns (bool, optional): Whether to log cumulative returns per episode.
                                      Defaults to False.

    Returns:
        np.ndarray: The learned Q-table, a 2D array of shape (n_states, n_actions).
                    If log_returns is True, also returns a list of cumulative rewards.
    """
    n_states, n_actions = env.size**2, len(ACTION_SPACE)
    Q = np.zeros((n_states, n_actions))
    returns_log = []

    rng = np.random.default_rng()
    for episode in range(params.episodes):
        s = env.reset()
        done = False
        cumulative_reward = 0
        while not done:
            # ε-greedy
            if rng.random() < params.epsilon:
                a = rng.integers(n_actions)
            else:
                a = int(np.argmax(Q[s]))
            s_next, r, done = env.step(a)
            Q[s, a] += params.alpha * (r + params.gamma * np.max(Q[s_next]) - Q[s, a])
            s = s_next
            cumulative_reward += r
        if log_returns:
            returns_log.append(cumulative_reward)

    if log_returns:
        return Q, returns_log
    return Q


def greedy_policy(Q: np.ndarray) -> List[int]:
    """Extract the greedy policy from a Q-table.

    For each state, this function selects the action with the highest Q-value.

    Args:
        Q (np.ndarray): The Q-table, a 2D array where Q[s, a] is the Q-value
                        of taking action a in state s.

    Returns:
        List[int]: A list where the i-th element is the greedy action to take
                   in state i.
    """
    return list(np.argmax(Q, axis=1))
