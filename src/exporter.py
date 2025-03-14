import pandas as pd

def save_rankings(tracks: dict) -> None:
    """
    Saves the rankings of the tracks to a CSV file.

    Args:
        tracks (dict): The dictionary containing track information.
        name (str): The name of the playlist.
    """
    ranked_tracks = sorted(
        tracks.values(), 
        key=lambda x: x['elo'], 
        reverse=True
    )

    df = pd.DataFrame(ranked_tracks)

    df['elo'] = df['elo'].round(0).astype(int)

    csv = df.to_csv(index=False).encode()

    return csv
