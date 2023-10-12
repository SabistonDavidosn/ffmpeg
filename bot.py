import os
import subprocess
import time

# Path to yt-dlp and ffmpeg executables
YTDL_PATH = 'yt-dlp'
FFMPEG_PATH = 'ffmpeg'

# Input file containing video links
INPUT_FILE = 'Input.txt'

# Output folder for compressed videos
OUTPUT_FOLDER = 'Done'

# Sleep time in seconds (24 hours)
SLEEP_TIME = 24 * 60 * 60

def download_video(link):
    # Construct yt-dlp command to download video in hd_mp4-1080p format
    command = [YTDL_PATH, '-f', 'hd_mp4-1080p', link]
    
    try:
        # Execute yt-dlp command
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to download video: {link}")
        return False

def compress_video(filename):
    # Construct ffmpeg command to compress the downloaded video using libx265 codec and CRF 31
    input_path = os.path.abspath(filename)
    output_path = os.path.join(OUTPUT_FOLDER, f"{os.path.splitext(filename)[0]}_compressed.mp4")
    
    command = [FFMPEG_PATH, '-i', input_path, '-vcodec', 'libx265', '-crf', '31', output_path]
    
    try:
        # Execute ffmpeg command
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to compress video: {filename}")
        return False

def main():
    # Create output folder if it doesn't exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    with open(INPUT_FILE) as file:
        links = file.readlines()
        
        for link in links:
            link = link.strip()
            
            if not link.startswith('#'):  # Skip commented lines in the input file
                
                while True:
                    if download_video(link):
                        break
                    
                    time.sleep(60)  # Retry after 1 minute if failed to download
                    
                filename = os.path.basename(link)
                
                while True:
                    if compress_video(filename):
                        break
                    
                    time.sleep(60)  # Retry after 1 minute if failed to compress
                
                print(f"Successfully processed: {link}")
                
                time.sleep(SLEEP_TIME)  # Sleep for 24 hours before processing the next video

if __name__ == '__main__':
    main()