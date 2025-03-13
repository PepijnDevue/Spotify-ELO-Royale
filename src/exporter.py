import csv

def save_rankings(tracks: list):
    """
    Saves the rankings of the tracks to a CSV file.

    Args:
        tracks (list): The list of tracks
    """
    ranked_tracks = sorted(tracks, key=lambda x: x['elo'], reverse=True)

    with open('playlist_rankings.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Rank', 'Track', 'Artist', 'Elo Rating'])

        for idx, track in enumerate(ranked_tracks, 1):
            writer.writerow([idx, track['name'], track['artist_name'], round(track['elo'])])
