import spotipy
from spotipy.oauth2 import SpotifyOAuth
from keys import client_id, client_secret

class SpotifyClient:
    """Handles authentication and data retrieval from Spotify API."""

    def __init__(self) -> None:
        """Initializes the Spotify API client."""
        self._sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri='http://localhost:8080',
            scope='playlist-read-private'
        ))

    def get_playlist_tracks(self, playlist_id: str) -> list:
        """Retrieves all tracks from a given playlist.

        Args:
            playlist_id: The Spotify playlist ID.

        Returns:
            A list of track items.
        """
        tracks = []
        results = self._sp.playlist_tracks(playlist_id)

        while results:
            tracks.extend(results['items'])
            results = self._sp.next(results)

        return tracks
