import os

from scripts.spotify_playlist import SpotifyPlaylistDownloader
from scripts.youtube_playlist import YouTubePlaylistDownloader


class PlaylistDownloader:
    def __init__(self):
        project_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_download_path = os.path.join(project_dir, "downloads")

    def download(self):
        print("\n📌 Download from Spotify or YouTube?")
        print("1️⃣ Spotify")
        print("2️⃣ YouTube")

        choice = input("\nEnter your choice (1/2): ").strip()
        playlist_url = input("Enter playlist URL: ")
        playlist_name = input("Enter the desired name for the playlist (press Enter to auto-generate): ")

        if choice == "1":
            SpotifyPlaylistDownloader(self.base_download_path, playlist_url, playlist_name).download_playlist()
        elif choice == "2":
            YouTubePlaylistDownloader(self.base_download_path, playlist_url, playlist_name).download()
        else:
            print("\n❌ Invalid choice! Please enter 1 or 2.")


if __name__ == "__main__":
    PlaylistDownloader().download()