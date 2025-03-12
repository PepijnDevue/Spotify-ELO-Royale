class Track:
    """Represents a track with name, artist, ID, and Elo rating."""

    def __init__(self, track_item: dict, elo: int = 1000) -> None:
        """
        Initializes a track.

        Args:
            track_item: The track item from Spotify API.
            elo: The initial Elo rating.
        """
        self.name = track_item["track"]["name"]
        self.artist = track_item["track"]["artists"][0]["name"]
        self.track_id = track_item["track"]["id"]
        self.elo = elo

    def __repr__(self) -> str:
        """Returns a string representation of the track."""
        return f"{self.name} by {self.artist} (Elo: {self.elo})"
