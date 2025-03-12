from src.ranking_system import RankingSystem

if __name__ == "__main__":
    playlist_link = input("Enter Spotify playlist link: ")
    ranking_system = RankingSystem(playlist_link)
    ranking_system.run()
