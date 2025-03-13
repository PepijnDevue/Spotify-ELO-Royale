import streamlit as st

from src import spotify_client, tournament, gui, exporter

# Streamlit app
st.title("Spotify ELO Royale 🎵")
st.write("Rank your favorite Spotify tracks using an ELO-based ranking system!")

# Get Spotify client
sp_client = spotify_client.load_client()

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
if "matches" not in st.session_state:
    st.session_state.matches = []

if playlist_url:
    if "tracks" not in st.session_state:
        st.session_state.tracks = spotify_client.get_playlist_tracks(sp_client, playlist_url)

    # Calculate max rounds
    max_rounds = max_rounds_inputs or tournament.calc_max_rounds()

    if st.session_state.current_round < max_rounds:
        
        if not st.session_state.matches:
            st.session_state.matches = tournament.get_swiss_pairings()

        st.write(f"Round: {st.session_state.current_round}/{max_rounds}")

        song_l_id, song_r_id = st.session_state.matches.pop(0)

        col1, col2 = st.columns(2)

        with col1:
            gui.display_track(song_l_id)
            if st.button("Select", key="select_a"):
                tournament.update_elo(song_l_id, song_r_id)

        with col2:
            gui.display_track(song_r_id)
            if st.button("Select", key="select_b"):
                tournament.update_elo(song_r_id, song_l_id)

        if not st.session_state.matches:
            st.session_state.current_round += 1

    else:
        playlist_name = sp_client.playlist(playlist_url)["name"]

        st.success(f"Tournament completed! Results saved to results/{playlist_name}.csv")

        exporter.save_rankings(st.session_state.tracks, name=playlist_name)