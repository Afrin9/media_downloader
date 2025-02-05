import os
import subprocess

# Function to download Spotify playlist
def download_spotify_playlist(playlist_url, output_path="D:/songs/audio"):
    # Ensure output directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    os.environ["FFMPEG_BINARY"] = r"C:\ffmpeg\ffmpeg-7.1-essentials_build\bin\ffmpeg.exe"

    # Run the SpotDL command using subprocess
    command = [
        "spotdl",
        playlist_url,  # Spotify Playlist URL
        "--output", os.path.join(output_path, "%(title)s.%(ext)s"),  # Output directory and file format
    ]

    # Execute the command to download the playlist
    try:
        subprocess.run(command, check=True)
        print("Download completed!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


# Get the playlist URL from the user
playlist_url = input("Enter the Spotify playlist URL: ")
download_spotify_playlist(playlist_url)

