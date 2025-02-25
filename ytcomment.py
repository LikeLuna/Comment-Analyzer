# these libraries help to import all requisites for the project
import subprocess
import sys

# Function to install missing packages
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
required_packages = ["google-api-python-client", "python-dotenv"]

# Check & install missing packages
for package in required_packages:
    try:
        __import__(package.replace("-", "_"))
    except ImportError:
       subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package],
            stdout=subprocess.DEVNULL,  # Suppress output
            stderr=subprocess.DEVNULL   # Suppress errors unless installation fails
        )

from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import re

load_dotenv(dotenv_path=".env")
API_KEY=os.getenv("API_KEY") # place yours here


def check_api_key():
    try:
        youtube = build("youtube", "v3", developerKey=API_KEY)
        request = youtube.channels().list(
            part="id",
            forUsername="YouTube"  # Checking YouTube's official channel
        )
        response = request.execute()
        print("API Key is valid!")
        print(response)
    except Exception as e:
        print("API Key is invalid or restricted.")
        print(e)

# Run the test
# check_api_key()


load_dotenv()
API_KEY=os.getenv("API_KEY")
#Replace with your actual YouTube API key

def extract_video_id(youtube_url):
    """Extracts the video ID from a YouTube URL."""
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, youtube_url)
    return match.group(1) if match else None

def get_youtube_comments(video_id, max_results=10):
    """Fetches comments from a YouTube video using the API."""
    youtube = build("youtube", "v3", developerKey=API_KEY)
    comments = []

    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results
        )
        response = request.execute()

        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
    except Exception as e:
        print("Error:", e)

    return comments

