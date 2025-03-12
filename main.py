import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv

from keys import client_id, client_secret

# Spotify API setup
def create_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri='http://localhost:8080',
        scope='playlist-read-private'
    ))

# Get playlist tracks with pagination
def get_playlist_tracks(sp, playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    while results:
        tracks.extend(results['items'])
        results = sp.next(results)
    return tracks

# Elo rating update calculation
def update_elo(winner, loser, k=32):
    r_winner = winner['elo']
    r_loser = loser['elo']
    
    expected_win = 1 / (1 + 10 ** ((r_loser - r_winner) / 400))
    winner['elo'] += k * (1 - expected_win)
    loser['elo'] += k * (-expected_win)

# Swiss-style pairing function
def get_swiss_pairings(tracks):
    tracks.sort(key=lambda x: x['elo'], reverse=True)
    pairings = []
    for i in range(0, len(tracks) - 1, 2):
        pairings.append((tracks[i], tracks[i + 1]))
    return pairings

def main():
    # Initialize Spotify client
    sp = create_spotify_client()
    
    # Get playlist ID from user
    playlist_link = input("Enter Spotify playlist link: ")
    playlist_id = playlist_link.split('/')[-1].split('?')[0]
    
    # Fetch playlist tracks
    print("Fetching playlist tracks...")
    raw_tracks = get_playlist_tracks(sp, playlist_id)
    
    if not raw_tracks:
        print("No tracks found in playlist!")
        return
    
    # Process tracks with initial Elo ratings
    tracks = []
    for item in raw_tracks:
        track = item['track']
        tracks.append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'id': track['id'],
            'elo': 1000  # Initial Elo rating
        })
    
    print(f"Loaded {len(tracks)} tracks for ranking!")
    
    rounds = 0
    max_rounds = 10  # Stop after a fixed number of rounds
    
    # Main comparison loop using Swiss pairing
    while len(tracks) > 1 and rounds < max_rounds:
        pairings = get_swiss_pairings(tracks)
        if not pairings:
            break
        
        for a, b in pairings:
            print("\nTrack 1:", f"{a['name']} by {a['artist']}")
            print("vs")
            print("Track 2:", f"{b['name']} by {b['artist']}")
            
            choice = input("Choose winner (1/2) or 'q' to quit: ").strip().lower()
            
            if choice == 'q':
                break
            elif choice == '1':
                update_elo(a, b)
                print(f"{a['name']} wins!")
            elif choice == '2':
                update_elo(b, a)
                print(f"{b['name']} wins!")
            else:
                print("Invalid choice. Please enter 1, 2, or q.")
        
        rounds += 1
        
        # Reduce the weakest tracks after a few rounds
        if rounds % 3 == 0 and len(tracks) > 2:
            print("Removing lowest-ranked track to refine rankings.")
            tracks = tracks[:-len(tracks)//5]  # Remove the track with lowest Elo
    
    # Sort tracks by Elo rating
    ranked_tracks = sorted(tracks, key=lambda x: x['elo'], reverse=True)
    
    # Save results to CSV
    with open('playlist_rankings.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Rank', 'Track', 'Artist', 'Elo Rating'])
        for idx, track in enumerate(ranked_tracks, 1):
            writer.writerow([idx, track['name'], track['artist'], round(track['elo'])])
    
    print("\nRanking complete! Results saved to playlist_rankings.csv")

if __name__ == "__main__":
    main()
