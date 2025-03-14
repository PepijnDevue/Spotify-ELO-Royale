import streamlit as st
from . import exporter

def display_header():
    """
    Displays the app title and description.
    """
    st.title("Spotify ELO Royale 🎵")
    st.write("Rank your favorite Spotify tracks using an ELO-based ranking system!")

def display_sidebar():
    """ 
    Displays the link input, options, and rankings.
    """
    # Sidebar input for Spotify playlist link
    playlist_url = st.sidebar.text_input("Enter Spotify Playlist Link")

    # Sidebar toggle for automatic max rounds calculation
    enable_auto_rounds = st.sidebar.checkbox("Automatically calculate max rounds", value=True)

    # Sidebar input for max rounds if automatic calculation is disabled
    max_rounds_inputs = None 
    if not enable_auto_rounds:
        max_rounds_inputs = st.sidebar.slider("Max Rounds", 3, 10, 3)

    return playlist_url, max_rounds_inputs

def display_rounds(max_rounds: int):
    """
    Displays the current round and max rounds.
    
    Args:
        max_rounds (int): The maximum number of rounds.
    """
    st.write(f"Round: {st.session_state.current_round}/{max_rounds}")

def display_track(track_id: str):
    """
    Displays the track information and an embedded Spotify player.
    
    Args:
        track_id (str): The track ID.
    """
    track = st.session_state.tracks[track_id]

    st.write(f"**{track['name']}**")
    st.write(f"by {track['artist_name']}")

    embed_url = f"https://open.spotify.com/embed/track/{track['id']}" 

    st.components.v1.iframe(embed_url, width=400, height=352, scrolling=False)

def display_download_button(playlist_name: str) -> None:
    """
    Displays a download button for the ranked playlist.
    """
    data = exporter.save_rankings(st.session_state.tracks)

    st.download_button(
        label="Download Rankings",
        data=data,
        file_name=f"{playlist_name}_rankings.csv",
        mime="text/csv"
    )