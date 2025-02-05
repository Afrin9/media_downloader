import yt_dlp
import os
import subprocess

def download_playlist(url, download_type="video"):
    if download_type == "audio":
        output_path = "D:/songs/audio"
    else:  # Default is video
        output_path = "D:/songs/video"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'ffmpeg_location': r'C:\ffmpeg\ffmpeg-7.1-essentials_build\bin'
    }

    if download_type == "audio":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
    else:
        ydl_opts.update({
            'format': 'bestvideo[height<=1080]+bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("Download completed!")

def download_spotify_playlist(playlist_url, output_path="D:/songs/audio"):

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

def main():
    platform= input("Enter '1' for Spotify or '2' for Others: : ").strip()

    if platform == "1":
        playlist_url = input("Enter the Spotify playlist URL: ")
        download_spotify_playlist(playlist_url)
    elif platform == "2":
        playlist_url = input("Enter the playlist URL: ")
        download_type = input("Enter 'video' to download videos or 'audio' for audio: ").strip().lower()
        download_playlist(playlist_url, download_type)

    else:
        print("Invalid option.")
    download_more= input("Do you want to download more songs? (y/n): ").strip().lower()
    if download_more == "y":
        main()
    else:
        print("Goodbye!")

main()
