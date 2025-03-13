import streamlit as st

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