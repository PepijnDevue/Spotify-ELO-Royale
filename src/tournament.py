import streamlit as st

import math

@st.cache_data
def calc_max_rounds(len_tracks: int) -> int:
    """
    Calculates the maximum number of rounds.
    If the input max_rounds is 0:
    the function calculates the maximum rounds based on the number of tracks.
    
    Args:
        len_tracks (int): The number of tracks.
    
    Returns:
        int: The maximum number of rounds.
    """
    return int(1.5 * math.log2(len_tracks))