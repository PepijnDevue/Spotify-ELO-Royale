import streamlit as st

def display_track(track: dict):
    """
    Displays the track information and an embedded Spotify player.
    
    Args:
        track (dict): The track information.
    """
    st.write(f"**{track['name']}**")
    st.write(f"by {track['artist_name']}")

    embed_url = f"https://open.spotify.com/embed/track/{track['id']}" 

    st.components.v1.iframe(embed_url, width=400, height=352, scrolling=False)