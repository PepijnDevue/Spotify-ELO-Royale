import streamlit as st

import spotipy
from spotipy.oauth2 import SpotifyOAuth

def load_client() -> spotipy.Spotify:
    """
    Initializes and returns a Spotipy client using credentials from Streamlit secrets.
    
    Returns:
        spotipy.Spotify: An authenticated Spotipy client.
    """
    auth_manager = SpotifyOAuth(
        client_id=st.secrets["SPOTIFY_CLIENT_ID"],
        client_secret=st.secrets["SPOTIFY_CLIENT_SECRET"],
        redirect_uri='https://spotify-elo-royale.streamlit.app',
        scope='playlist-read-private'
    )

    client = spotipy.Spotify(auth_manager=auth_manager)

    return client

def get_playlist_tracks(playlist_url: str) -> dict:
    """
    Fetches tracks from a given Spotify playlist URL.
    
    Args:
        playlist_url (str): The URL of the Spotify playlist.
    
    Returns:
        dict: A dictionary containing track information.
    """
    try:
        print("Fetching playlist tracks...")

        client = st.session_state.sp_client

        playlist_id = _get_playlist_id(playlist_url)
        results = client.playlist_tracks(playlist_id)

        print(type(results))

        # Extract track information
        tracks = {}
        while results:
            print(type(client.next(results)))
            tracks.update(_get_track_info(results['items']))
            results = client.next(results)
            print(results)

        return tracks
    
    except Exception as e:
        st.error(f"Error fetching playlist tracks: {e}")
        return {}

def _get_track_info(tracks: list) -> dict:
    """Extracts track information from the given list of track items.
    Track info includes the track ID, name, and artist name, elo.

    Args:
        tracks (list): List of track items from the Spotify playlist API response.

    Returns:
        dict: A dictionary containing track information.
    """
    track_info = {}

    for track in tracks:
        track_id = track["track"]["id"]
        track_info[track_id] = {
            "id": track["track"]["id"],
            "name": track["track"]["name"],
            "artist_name": track["track"]["artists"][0]["name"],
            "elo": 1000
        }
    
    return track_info

def _get_playlist_id(playlist_url: str) -> str:
    """Extracts the playlist ID from the given Spotify playlist URL.
    
    Args:
        playlist_url (str): The URL of the Spotify playlist.
    
    Returns:
        str: The playlist ID.
    """
    return playlist_url.split("playlist/")[-1].split("?")[0]