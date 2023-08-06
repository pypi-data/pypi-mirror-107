"""Piglr Game module."""

import random
from typing import Union

from piglr.state import State, as_dict
from piglr.error import IllegalParameterError


class Game:
    """Game class used to interact with a the pig environment.

    Example usage:
    
    >>> import json
    >>> import random
    >>> import piglr
    >>> game = piglr.Game()
    >>> obs, winner = game.reset()
    >>> while winner is None:
    >>>     roll = random.randint(0, 1)
    >>>     if roll:
    >>>         obs, winner = game.roll()
    >>>     else:
    >>>         obs, winner = game.bank()
    >>> print(json.dumps(obs, indent=4))
    >>> print(f'Winner: {winner}')

    """
    def __init__(self, players: int = 2, num_dice: int = 1, dn: int = 6, target: int = 100):
        """`Game` init method.

        Args:
            players: Number of players. (Legal range 2-inf)
            num_dice: Number of dice. (Legal range 1-inf)
            dn: Dice sidedness (Think D&D, d6, d8, d20, etc.). (Legal
                range 1-inf)
            target: Target score for the game. (Legal range 1-inf)

        Raises:
            TypeError: TypeError is raised whenever one of the passed
                parameters is not of type int.
            piglr.error.IllegalParameterError: is raised whenever a
                parameter is passed an illegal value. For legal values
                see args section of init method.

        """
        for param in [players, num_dice, dn, target]:
            if not isinstance(param, int):
                param_name = f'{param}='.split('=')[0]
                raise TypeError(f'Param {param_name} must be of type int')

        if players < 2:
            raise IllegalParameterError('There must be at least 2 players')

        if num_dice < 1:
            raise IllegalParameterError('There must be at least 1 dice')

        if dn < 2:
            raise IllegalParameterError('The dice must be at least 2 sided')

        if target < 1:
            raise IllegalParameterError('The target must be positive')

        self.players = players
        self.num_dice = num_dice
        self.dn = dn
        self.target = target

    @property
    def state(self) -> dict:
        """State property.

        Returns:
            Instance of :obj:`piglr.state.State` converted to a
            dictionary.

        """
        return as_dict(self._state)

    def _increment_turn(self, bank: bool) -> None:
        if bank:
            self._state.score[self._state.turn] += self._state.bank

        self._state.rolls = 0
        self._state.bank = 0

        if self._state.players - 1 == self._state.turn:
            self._state.turn = 0
        else:
            self._state.turn += 1

    def _check_for_winner(self) -> Union[int, None]:
        if max(self._state.score.values()) >= self._state.target:
            return max(self._state.score, key=self._state.score.get)
        return None

    def reset(self) -> Union[dict, None]:
        """Reset method.

        Resets the game state.

        Returns:
            - State property :attr:`piglr.game.Game.state`.
            - :obj:`None`.

        """
        self._state = State(
            players=self.players,
            num_dice=self.num_dice,
            dn=self.dn,
            score={i:0 for i in range(self.players)},
            target=self.target
        )

        return self.state, None

    def roll(self) -> Union[dict, None]:
        """Roll dice.

        Rolls dice for current player.

        Returns:
            - State property :attr:`piglr.game.Game.state`.
            - :obj:`None`.

        """
        for _ in range(self._state.num_dice):
            d = random.randint(1, self._state.dn)
            if d == 1:
                self._increment_turn(bank=False)
                return self.state, None

            else:
                self._state.rolls += 1
                self._state.bank += d

        return self.state, None
    
    def bank(self) -> Union[dict, Union[int, None]]:
        """Scores bank.

        Scores bank for current player.        

        Returns:
            - State property :attr:`piglr.game.Game.state`.
            - :obj:`int` if the game has been won else :obj:`None`.

        """
        self._increment_turn(bank=True)

        winner = self._check_for_winner()

        return self.state, winner
