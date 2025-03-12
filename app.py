import streamlit as st
from src.ranking_system import RankingSystem
from src.track import Track

# Streamlit app
st.title("Spotify ELO Royale 🎵")
st.write("Rank your favorite Spotify tracks using an ELO-based ranking system!")

# Input: Spotify Playlist Link
playlist_link = st.text_input("Enter Spotify Playlist Link", "")

if playlist_link:
    # Initialize ranking system
    ranking_system = RankingSystem(playlist_link)
    
    # Show Playlist Info
    st.write("Number of tracks:", len(ranking_system._tracks))

    # Initialize state for rounds
    if "rounds" not in st.session_state:
        st.session_state.rounds = 0
    if "pairings" not in st.session_state:
        st.session_state.pairings = []
    if "ranked_tracks" not in st.session_state:
        st.session_state.ranked_tracks = []

    # Generate Swiss Pairings
    if len(ranking_system._tracks) > 1 and st.session_state.rounds < ranking_system._max_rounds:
        if not st.session_state.pairings:
            st.session_state.pairings = ranking_system._get_swiss_pairings()

        # Display current pairing
        current_pair = st.session_state.pairings.pop(0)
        track_a, track_b = current_pair

        # Song Preview
        def display_track(track: Track):
            st.write(f"**{track.name}** by {track.artist}")
            
            if track.embed_url:
                st.components.v1.iframe(track.embed_url, width=400, height=352, scrolling=False)
            else:
                st.write("No preview available.")

        st.subheader("Choose the Winner:")
        col1, col2 = st.columns(2)

        with col1:
            display_track(track_a)
            if st.button(f"Select: {track_a.name}", key=f"select_{track_a.id}"):
                ranking_system._elo_system.update_elo(track_a, track_b)
                st.session_state.rounds += 1
                st.experimental_rerun()

        with col2:
            display_track(track_b)
            if st.button(f"Select: {track_b.name}", key=f"select_{track_b.id}"):
                ranking_system._elo_system.update_elo(track_b, track_a)
                st.session_state.rounds += 1
                st.experimental_rerun()

    # Save Rankings
    if len(ranking_system._tracks) <= 1 or st.session_state.rounds >= ranking_system._max_rounds:
        ranking_system._save_rankings()
        st.success("Ranking complete! Results saved to `playlist_rankings.csv`.")
        st.write("Check the CSV file for the final rankings!")