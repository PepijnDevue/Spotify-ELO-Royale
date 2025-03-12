import math
import csv
from .spotify_client import SpotifyClient
from .track import Track
from .elo_system import EloSystem

class RankingSystem:
    """Manages the ranking process of tracks using the Elo system."""

    def __init__(self, playlist_link: str, k_factor: int = 32) -> None:
        """Initializes the ranking system.

        Args:
            playlist_link: The Spotify playlist link.
            k_factor: The Elo ranking K-factor.
        """
        self._spotify_client = SpotifyClient()
        self._playlist_id = self._extract_playlist_id(playlist_link)

        self._elo_system = EloSystem(k_factor)

        self._tracks = self._init_tracks()

        self._max_rounds = self._calc_max_rounds()

        self._ranked_tracks = []

    def _calc_max_rounds(self):
        """
        Calculates the maximum number of rounds based on the number of tracks.
        
        Returns:
            The maximum number of rounds.
        """
        len_tracks = len(self._tracks)

        max_rounds_log = int(1.5 * math.log2(len_tracks))

        return min(10, max_rounds_log)

    def _extract_playlist_id(self, playlist_link: str) -> str:
        """Extracts the playlist ID from the given Spotify playlist link.

        Args:
            playlist_link: The Spotify playlist link.

        Returns:
            The extracted playlist ID.
        """
        return playlist_link.split('/')[-1].split('?')[0]

    def _init_tracks(self) -> list[Track]:
        """Fetches tracks from the playlist and initializes their Elo ratings.

        Returns:
            A list of Track objects.
        """
        raw_tracks = self._spotify_client.get_playlist_tracks(self._playlist_id)

        if not raw_tracks:
            print("No tracks found in playlist!")
            return []

        tracks = [Track(item) for item in raw_tracks]

        return tracks

    def _get_swiss_pairings(self) -> list[list[Track]]:
        """Creates track pairings based on the Swiss system ranking method.

        Returns:
            A list of track pair tuples.
        """
        self._tracks.sort(key=lambda x: x.elo, reverse=True)

        tournament = []
        for i in range(0, len(self._tracks) - 1, 2):
            tournament.append([
                self._tracks[i], 
                self._tracks[i + 1]
            ])

        return tournament

    def _save_rankings(self) -> None:
        """Saves the final track rankings to a CSV file."""
        # Extend the ranked tracks with any remaining unreduced tracks
        self._ranked_tracks.extend(self._tracks)

        ranked_tracks = sorted(self._ranked_tracks, key=lambda x: x.elo, reverse=True)

        with open('playlist_rankings.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Rank', 'Track', 'Artist', 'Elo Rating'])

            for idx, track in enumerate(ranked_tracks, 1):
                writer.writerow([idx, track.name, track.artist, round(track.elo)])

        print("\nRanking complete! Results saved to playlist_rankings.csv")

    def run(self) -> None:
        """Runs the ranking process, allowing the user to choose winners."""
        rounds = 0

        while len(self._tracks) > 1 and rounds < self._max_rounds:
            pairings = self._get_swiss_pairings()

            for a, b in pairings:
                print(f"\nTrack 1: {a.name} by {a.artist}")
                print("vs")
                print(f"Track 2: {b.name} by {b.artist}")

                choice = input("Choose winner (1/2) or 'q' to quit: ").strip().lower()

                if choice == 'q':
                    return
                if choice == '1':
                    self._elo_system.update_elo(a, b)
                    print(f"{a.name} wins!")
                elif choice == '2':
                    self._elo_system.update_elo(b, a)
                    print(f"{b.name} wins!")
                else:
                    print("Invalid choice. Please enter 1, 2, or q.")

            rounds += 1

        self._save_rankings()
