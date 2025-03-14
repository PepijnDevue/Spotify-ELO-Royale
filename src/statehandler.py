import streamlit as st

from . import spotify

def init_session_state():
    """
    Initializes session state variables.
    """
    set_session_state("sp_client", spotify.load_client())
    set_session_state("current_round", 0)
    set_session_state("matches", [])

def set_session_state(key: str, value: any):
    """
    Sets a session state variable if it does not exist."
    """
    if key not in st.session_state:
        st.session_state[key] = value