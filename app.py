import streamlit as st

from src import tournament, gui, spotify

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
    gui.display_rounds(max_rounds)

    if st.session_state.current_round <= max_rounds:
        
        if not st.session_state.matches:
            st.session_state.matches = tournament.get_swiss_pairings()
            st.session_state.current_round += 1

        tournament.play_match()

    else:
        playlist_name = spotify.get_playlist_name()
        gui.display_download_button(playlist_name)