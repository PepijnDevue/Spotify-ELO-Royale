import streamlit as st

from src.spotify_client import load_spotify_client, get_playlist_tracks

from src.tournament import calc_max_rounds, get_swiss_pairings, update_elo

from src.gui import display_track

from src.exporter import save_rankings

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

# save to state
if "current_round" not in st.session_state:
    st.session_state.current_round = 0
if "tracks" not in st.session_state:
    st.session_state.tracks = []
if "tournament" not in st.session_state:
    st.session_state.tournament = []


if playlist_url:
    st.session_state.tracks = get_playlist_tracks(sp_client, playlist_url)
    
    # Calculate max rounds
    max_rounds = max_rounds_inputs or calc_max_rounds()

    if st.session_state.current_round < max_rounds:
        
        if not st.session_state.tournament:
            st.session_state.tournament = get_swiss_pairings()

        song_a, song_b = st.session_state.tournament.pop(0)

        st.subheader(f"Choose the better song:")

        col1, col2 = st.columns(2)

        with col1:
            display_track(song_a)
            if st.button("Select", key="select_a"):
                update_elo(song_a, song_b)
                st.session_state.current_round += 1
                st.rerun()

        with col2:
            display_track(song_b)
            if st.button("Select", key="select_b"):
                update_elo(song_b, song_a)
                st.session_state.current_round += 1
                st.rerun()

    else:
        st.success("Tournament completed! Results saved to playlist_rankings.csv")

        save_rankings(st.session_state.tracks)