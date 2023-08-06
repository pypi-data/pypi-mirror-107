"""Piglr gamestate module."""

from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class State:
    """Piglr state dataclass."""
    players: int
    """Number of players."""
    num_dice: int
    """Number of dice."""
    dn: int
    """Dice sidedness (Think D&D, d6, d8, d20, etc.)."""
    score: Dict[int, int]
    """Current game score."""
    target: int
    """Target score for the game."""
    turn: int = 0
    """Active player (who's turn is it)."""
    rolls: int = 0
    """Number of time's active player has rolled."""
    bank: int = 0
    """Active player's bank."""


def as_dict(state: State) -> dict:
    """See :func:`dataclasses.asdict`."""
    return asdict(state)
