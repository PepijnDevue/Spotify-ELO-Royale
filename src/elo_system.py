from .track import Track

class EloSystem:
    """Manages Elo rating calculations and ranking logic."""

    def __init__(self, k_factor: int = 32) -> None:
        """Initializes the Elo ranking system.

        Args:
            k_factor: The Elo ranking K-factor.
        """
        self._k_factor = k_factor

    def update_elo(self, winner: Track, loser: Track) -> None:
        """Updates the Elo ratings based on the match outcome.

        Args:
            winner: The winning track.
            loser: The losing track.
        """
        r_winner = winner.elo
        r_loser = loser.elo

        expected_win = 1 / (1 + 10 ** ((r_loser - r_winner) / 400))

        winner.elo += self._k_factor * (1 - expected_win)
        loser.elo += self._k_factor * (-expected_win)
