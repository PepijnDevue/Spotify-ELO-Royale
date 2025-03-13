import csv

def _get_swiss_pairings(tracks):
    tracks.sort(key=lambda x: x['elo'], reverse=True)

    tournament = []
    for i in range(0, len(tracks) - 1, 2):
        tournament.append([
            tracks[i], 
            tracks[i + 1]
        ])

    return tournament

def _save_rankings(tracks):
    ranked_tracks = sorted(tracks, key=lambda x: x.elo, reverse=True)

    with open('playlist_rankings.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Rank', 'Track', 'Artist', 'Elo Rating'])

        for idx, track in enumerate(ranked_tracks, 1):
            writer.writerow([idx, track['name'], track['artist'], round(track['elo'])])

def update_elo(winner, loser):
    r_winner = winner['elo']
    r_loser = loser['elo']

    expected_win = 1 / (1 + 10 ** ((r_loser - r_winner) / 400))

    winner['elo'] += 32 * (1 - expected_win)
    loser['elo'] += 32 * (-expected_win)