import streamlit as st

from src.spotify_client import load_spotify_client, get_playlist_tracks

from src.tournament import calc_max_rounds

# Streamlit app
st.title("Spotify ELO Royale 🎵")
st.write("Rank your favorite Spotify tracks using an ELO-based ranking system!")

# Get Spotify client
sp_client = load_spotify_client()

# Sidebar input for Spotify playlist link
playlist_url = st.sidebar.text_input("Enter Spotify Playlist Link")

# Sidebar toggle for automatic max rounds calculation
enable_auto_rounds = st.sidebar.checkbox("Automatically calculate max rounds", value=True)

# Sidebar input for max rounds if automatic calculation is disabled
max_rounds_inputs = None 
if not enable_auto_rounds:
    max_rounds_inputs = st.sidebar.slider("Max Rounds", 3, 10, 3)

if playlist_url:
    tracks = get_playlist_tracks(sp_client, playlist_url)
    
    # Calculate max rounds
    max_rounds = max_rounds_inputs or calc_max_rounds(len(tracks))

    