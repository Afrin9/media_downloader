import yt_dlp
import os
import re
import subprocess
import tkinter as tk
from tkinter import filedialog

from dotenv import load_dotenv
load_dotenv()
ffmpeg_path = os.getenv("FFMPEG_PATH")

class YouTubePlaylistDownloader:
    def __init__(self, save_path, playlist_url, download_type="video"):
        self.save_path = save_path
        self.playlist_url = playlist_url
        self.download_type = download_type

    def get_download_path(self):
        # folder_name = "audio" if self.download_type == "audio" else "video"
        download_folder =self.save_path
        os.makedirs(download_folder, exist_ok=True)
        return download_folder

    def download_playlist(self):
        download_path = self.get_download_path()
        print(f"Downloading YouTube playlist to: {download_path}")

        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'ffmpeg_location': ffmpeg_path
        }

        if self.download_type == "audio":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }]
            })
        else:
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
            })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.playlist_url])
            print("Download completed!")
        except Exception as e:
            print(f"Error downloading YouTube playlist: {e}")


class SpotifyPlaylistDownloader:
    def __init__(self, save_path, playlist_url, playlist_name=None):
        self.save_path = save_path
        self.playlist_url = playlist_url
        self.playlist_name = playlist_name or self.extract_playlist_name()

    def extract_playlist_name(self):
        match = re.search(r"(?<=playlist/)([A-Za-z0-9_-]+)", self.playlist_url)
        return match.group(0) if match else "unknown_playlist"

    def get_download_path(self):
        download_folder =self.save_path
        os.makedirs(download_folder, exist_ok=True)
        return download_folder

    def download_playlist(self):
        download_path = self.get_download_path()
        print(f"Downloading Spotify playlist to: {download_path}")

        command = [
            "spotdl",
            self.playlist_url,
            "--output", download_path
        ]

        try:
            subprocess.run(command, check=True)
            print("Download completed!")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading Spotify playlist: {e}")

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    return folder_selected


def main():

    while True:
        choice = input("1️⃣ Spotify or 2️⃣ YouTube \nEnter your choice (1/2):").strip()

        if choice == "1":
            playlist_name = input("Enter a name for the playlist (or press Enter to use default): ").strip() or None
            playlist_url = input("Enter the playlist URL: ").strip()
            print("Select the folder where files should be saved.")
            save_path = select_folder()
            if not save_path:
                print("No folder selected. Exiting...")
                break
            spotify_downloader = SpotifyPlaylistDownloader(save_path, playlist_url, playlist_name)
            spotify_downloader.download_playlist()

        elif choice == "2":
            download_type = input("Enter 'video' to download videos or 'audio' for audio: ").strip().lower()
            playlist_url = input("Enter the playlist URL: ").strip()
            print("Select the folder where files should be saved.")
            save_path = select_folder()
            if not save_path:
                print("No folder selected. Exiting...")
                break
            youtube_downloader = YouTubePlaylistDownloader(save_path, playlist_url, download_type)
            youtube_downloader.download_playlist()

        else:
            print("❌ Invalid option. Please try again.")


        download_more = input("Do you want to download more playlists? (y/n): ").strip().lower()
        if download_more != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
