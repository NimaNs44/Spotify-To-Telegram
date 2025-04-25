import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from telethon import TelegramClient, sync
from telethon.tl.functions.account import UpdateProfileRequest
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

# Telegram API credentials
TELEGRAM_API_ID = int(os.getenv('TELEGRAM_API_ID'))
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
TELEGRAM_PHONE = os.getenv('TELEGRAM_PHONE')

# Initialize Spotify client
scope = "user-read-currently-playing"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=scope
))

# Initialize Telegram client
client = TelegramClient('spotify_session', TELEGRAM_API_ID, TELEGRAM_API_HASH)
client.start(phone=TELEGRAM_PHONE)

# Keep track of the current song
current_song = ""

print("🎵 Spotify to Telegram Bio Updater 🎵")
print("Starting up and connecting to services...")

def update_bio(song_info):
    """Update Telegram bio with the current song info"""
    bio_text = f"🎧 Listening to: {song_info}"
    client(UpdateProfileRequest(about=bio_text))
    print(f"Bio updated: {bio_text}")

def get_current_song():
    """Get the currently playing song from Spotify"""
    try:
        current_track = sp.current_user_playing_track()
        if current_track is not None and current_track['is_playing']:
            artist = current_track['item']['artists'][0]['name']
            song = current_track['item']['name']
            return f"{song} - {artist}"
        return None
    except Exception as e:
        print(f"Error fetching current song: {e}")
        return None

def main():
    global current_song
    
    print("Connected! Monitoring your Spotify activity...")
    
    try:
        while True:
            song_info = get_current_song()
            
            if song_info:
                if song_info != current_song:
                    current_song = song_info
                    update_bio(current_song)
            else:
                if current_song != "":
                    current_song = ""
                    client(UpdateProfileRequest(about=""))
                    print("No song playing, bio cleared")
            
            # Wait for 30 seconds before checking again
            time.sleep(30)
    
    except KeyboardInterrupt:
        print("\nExiting program...")
        client.disconnect()
        print("Disconnected from Telegram")
        print("Goodbye!")

if __name__ == "__main__":
    main()