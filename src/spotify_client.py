import streamlit as st

import json

import spotipy
from spotipy.oauth2 import SpotifyOAuth

@st.cache_data
def load_spotify_client() -> spotipy.Spotify:
    """
    Initializes and returns a Spotipy client using credentials from Streamlit secrets.
    
    Returns:
        spotipy.Spotify: An authenticated Spotipy client.
    """
    auth_manager = SpotifyOAuth(
        client_id=st.secrets["SPOTIFY_CLIENT_ID"],
        client_secret=st.secrets["SPOTIFY_CLIENT_SECRET"],
        redirect_uri='http://localhost:8080',
        scope='playlist-read-private'
    )

    client = spotipy.Spotify(auth_manager=auth_manager)

    return client

@st.cache_data
def get_playlist_tracks(_client: spotipy.Spotify, playlist_url: str) -> list:
    """
    Fetches tracks from a given Spotify playlist URL.
    
    Args:
        client (spotipy.Spotify): An authenticated Spotipy client.
        playlist_url (str): The URL of the Spotify playlist.
    
    Returns:
        list: A list of track dictionaries containing track metadata.
    """
    playlist_id = _get_playlist_id(playlist_url)

    tracks = []
    results = _client.playlist_tracks(playlist_id)

    while results:
        tracks.extend(_get_track_info(results['items']))
        results = _client.next(results)

    return tracks

def _get_track_info(tracks: list) -> list:
    """Extracts track information from the given list of track items.
    Track info includes the track ID, name, and artist name, elo.

    Args:
        tracks (list): List of track items from the Spotify playlist API response.

    Returns:
        list: List of dictionaries containing track metadata.
    """
    track_info = []

    for track in tracks:
        track_info.append({
            "id": track["track"]["id"],
            "name": track["track"]["name"],
            "artist_name": track["track"]["artists"][0]["name"],
            "elo": 1000
        })
    
    return track_info

def _get_playlist_id(playlist_url: str) -> str:
    """Extracts the playlist ID from the given Spotify playlist URL.
    
    Args:
        playlist_url (str): The URL of the Spotify playlist.
    
    Returns:
        str: The playlist ID.
    """
    return playlist_url.split("playlist/")[-1].split("?")[0]