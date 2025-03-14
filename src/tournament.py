import streamlit as st

import math
import random

import gui

def play_match():
    """
    Plays a match between two tracks and updates the ELO ratings.
    """
    song_l_id, song_r_id = st.session_state.matches.pop(0)

    col1, col2 = st.columns(2)

    with col1:
        gui.display_track(song_l_id)
        if st.button("Select", key="select_a"):
            update_elo(song_l_id, song_r_id)

    with col2:
        gui.display_track(song_r_id)
        if st.button("Select", key="select_b"):
            update_elo(song_r_id, song_l_id)

@st.cache_data
def calc_max_rounds(max_round_inputs: None|int) -> int:
    """
    Calculates the maximum number of rounds.
    If the input max_rounds is 0:
    the function calculates the maximum rounds based on the number of tracks.
    
    Args:
        max_round_inputs (None|int): The input max rounds.
    
    Returns:
        int: The maximum number of rounds.
    """
    if max_round_inputs:
        return max_round_inputs

    len_tracks = len(st.session_state.tracks)
    return int(1.5 * math.log2(len_tracks))

def get_swiss_pairings() -> list:
    """
    Gets the swiss pairings for the tournament.

    Returns:
        list: A list of track_id pairs for the tournament.
    """
    sorted_tracks = sorted(
        st.session_state.tracks.values(),
        key=lambda x: x['elo'],
        reverse=True
    )

    tournament = []
    for i in range(0, len(sorted_tracks) - 1, 2):
        tournament.append([
            sorted_tracks[i]["id"], 
            sorted_tracks[i + 1]["id"]
        ])

    random.shuffle(tournament)

    return tournament

def update_elo(winner_id: str, loser_id: str):
    """
    Updates the ELO ratings of the winner and loser.

    Args:
        winner (dict): The winner's track information.
        loser (dict): The loser's track information.
    """
    winner_elo = st.session_state.tracks[winner_id]['elo']
    loser_elo = st.session_state.tracks[loser_id]['elo']

    expected_win = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))

    winner_add = 32 * (1 - expected_win)
    loser_add = 32 * (-expected_win)

    st.session_state.tracks[winner_id]['elo'] += winner_add
    st.session_state.tracks[loser_id]['elo'] += loser_add