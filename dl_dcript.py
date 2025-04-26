import subprocess
import os

# Directory to save downloaded albums
SAVE_DIR = "/home/fuckoff/Music"
# Path to the playlist links file
PLAYLIST_FILE = "/home/fuckoff/Public/music downloader/yt_playlist_list.txt"

def sanitize_filename(name):
    return "".join(c for c in name if c not in r'\/:*?"<>|').strip()

def download_playlists(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    
    for url in urls:
        print(f"\nProcessing playlist: {url}")
        
        # Get playlist title (first item only)
        result = subprocess.run(
            ["yt-dlp", "--print", "%(playlist_title)s", "--playlist-items", "1", url],
            capture_output=True,
            text=True
        )
        album_name = sanitize_filename(result.stdout.strip() or "Unknown_Album")
        album_path = os.path.join(SAVE_DIR, album_name)

        if os.path.isdir(album_path):
            print(f"Skipping '{album_name}' — already exists.")
            continue

        print(f"Downloading into: {album_path}")
        os.makedirs(album_path, exist_ok=True)

        command = [
            "yt-dlp",
            "-f", "bestaudio",
            "-x", "--audio-format", "mp3", "--audio-quality", "0",
            "--embed-metadata",
            "-o", f"{album_path}/%(playlist_index)03d - %(title)s.%(ext)s",
            url
        ]
        
        subprocess.run(command)

if __name__ == "__main__":
    download_playlists(PLAYLIST_FILE)
