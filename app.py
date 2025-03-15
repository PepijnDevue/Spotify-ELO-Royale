import streamlit as st

from src import tournament, gui, spotify, statehandler

gui.display_header()

playlist_url, max_rounds_inputs = gui.display_sidebar()

statehandler.init_session_state()

if playlist_url:
    statehandler.set_session_state("tracks", spotify.get_playlist_tracks(playlist_url))
    print(f"tr: {st.session_state.tracks}")

    max_rounds = tournament.calc_max_rounds(max_rounds_inputs)

    print(f"cr: {st.session_state.current_round}")
    if st.session_state.current_round <= max_rounds and tournament.len_playlist() > 1:
        
        gui.display_rounds(max_rounds)
        print("--")
        print(st.session_state.matches)
        if not st.session_state.matches:
            st.session_state.matches = tournament.get_swiss_pairings()
            st.session_state.current_round += 1
            print(st.session_state.matches)

        tournament.play_match()

    else:
        playlist_name = spotify.get_playlist_name(playlist_url)
        gui.display_download_button(playlist_name)