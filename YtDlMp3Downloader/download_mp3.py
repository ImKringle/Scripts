import os
import sys
import subprocess
import re
from yt_dlp import YoutubeDL

def sanitize_filename(filename):
    """Sanitize the filename to avoid special characters and spaces."""
    return re.sub(r'[^\w\-_.]', '_', filename)

def download_audio(video_url):
    try:
        # Define a temporary filename template
        temp_filename = "download.%(ext)s"
        
        # yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': temp_filename,  # Force download under a generic name
        }

        # Download the video
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', 'audio')
            downloaded_ext = info_dict.get('ext', 'webm')  # File extension from yt-dlp

        # Construct the temporary filename and sanitized final filename
        temp_file = f"download.{downloaded_ext}"
        sanitized_file = f"{sanitize_filename(video_title)}.mp3"

        # Convert to MP3
        convert_to_mp3(temp_file, sanitized_file)

        print(f"Converted to: {sanitized_file}")

    except Exception as e:
        print(f"An error occurred during download: {e}")

def convert_to_mp3(input_file, output_file):
    """Convert a downloaded audio file to MP3 format."""
    try:
        # Detect FFmpeg path
        ffmpeg_path = "ffmpeg.exe"  # Ensure ffmpeg.exe is in the same directory

        # Run FFmpeg conversion
        result = subprocess.run(
            [ffmpeg_path, '-i', input_file, output_file],
            text=True,
            capture_output=True
        )

        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            raise Exception("FFmpeg failed to convert the file.")
        
        # Clean up temporary file
        if os.path.exists(input_file):
            os.remove(input_file)

    except FileNotFoundError:
        print("FFmpeg executable not found. Ensure ffmpeg.exe is in the same directory.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python download_mp3.py <YouTube-URL>")
        sys.exit(1)

    video_url = sys.argv[1]
    download_audio(video_url)
    print("Download completed!")
