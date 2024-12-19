import os
from pytubefix import YouTube
import subprocess

def download_youtube_video(url, output_path="./videos"):
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)

        print(f"Fetching video details for: {url}")
        yt = YouTube(url)

        # Get the highest resolution video stream
        video_stream = yt.streams.filter(adaptive=True, file_extension="mp4", res="1080p").first()
        if not video_stream:
            print("1080p video stream not available for this video.")
            return

        # Get the audio stream
        audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()
        
        print("Downloading video...")
        video_path = video_stream.download(output_path, filename="video.mp4")

        print("Downloading audio...")
        audio_path = audio_stream.download(output_path, filename="audio.mp4")

        # Output file path
        final_output_path = os.path.join(output_path, f"{yt.title}.mp4")

        print("Merging video and audio using ffmpeg...")
        subprocess.run([
            "ffmpeg", "-i", video_path, "-i", audio_path, "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", final_output_path
        ])

        # Cleanup temporary files
        os.remove(video_path)
        os.remove(audio_path)

        print(f"Download complete: {final_output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    download_youtube_video(video_url)
