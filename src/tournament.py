import streamlit as st

import math

@st.cache_data
def calc_max_rounds() -> int:
    """
    Calculates the maximum number of rounds.
    If the input max_rounds is 0:
    the function calculates the maximum rounds based on the number of tracks.
    
    Args:
        len_tracks (int): The number of tracks.
    
    Returns:
        int: The maximum number of rounds.
    """
    len_tracks = len(st.session_state.tracks)
    return int(1.5 * math.log2(len_tracks))

def get_swiss_pairings() -> list:
    """
    Gets the swiss pairings for the tournament.

    Returns:
        list: The swiss pairings.
    """
    st.session_state.tracks.sort(key=lambda x: x['elo'], reverse=True)

    tournament = []
    for i in range(0, len(st.session_state.tracks) - 1, 2):
        tournament.append([
            st.session_state.tracks[i], 
            st.session_state.tracks[i + 1]
        ])

    return tournament

def update_elo(winner: dict, loser: dict):
    """
    Updates the ELO ratings of the winner and loser.

    Args:
        winner (dict): The winner's track information.
        loser (dict): The loser's track information.
    """
    r_winner = winner['elo']
    r_loser = loser['elo']

    expected_win = 1 / (1 + 10 ** ((r_loser - r_winner) / 400))

    winner['elo'] += 32 * (1 - expected_win)
    loser['elo'] += 32 * (-expected_win)