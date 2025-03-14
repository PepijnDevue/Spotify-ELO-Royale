import streamlit as st

from src import tournament, gui, exporter, spotify

def set_session_state(key: str, value: any):
    """
    Sets a session state variable if it does not exist."
    """
    if key not in st.session_state:
        st.session_state[key] = value

gui.display_header()

playlist_url, max_rounds_inputs = gui.display_sidebar()

# Initialize session state variables
set_session_state("sp_client", spotify.load_client())
set_session_state("current_round", 0)
set_session_state("matches", [])

if playlist_url:
    set_session_state("tracks", spotify.get_playlist_tracks(playlist_url))

    max_rounds = tournament.calc_max_rounds(max_rounds_inputs)

    if st.session_state.current_round < max_rounds:
        
        if not st.session_state.matches:
            st.session_state.matches = tournament.get_swiss_pairings()

        gui.display_rounds(max_rounds)

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
        playlist_name = st.session_state.sp_client.playlist(playlist_url)["name"]

        st.success(f"Tournament completed! Results saved to results/{playlist_name}.csv")

        exporter.save_rankings(st.session_state.tracks, name=playlist_name)