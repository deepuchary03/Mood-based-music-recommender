import os
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from typing import List, Dict, Any

# Define mood to genre/tag mappings
MOOD_MAPPINGS = {
    "Happy": ["pop", "happy", "feel good", "disco", "cheerful"],
    "Energetic": ["rock", "dance", "electronic", "workout", "energetic"],
    "Relaxed": ["chill", "ambient", "acoustic", "relaxing", "mellow"],
    "Calm": ["classical", "instrumental", "ambient", "meditation", "piano"],
    "Sad": ["sad", "melancholy", "ballad", "emotional", "blues"],
    "Anxious": ["intense", "alternative", "experimental", "dark", "heavy"],
    "Focused": ["study", "instrumental", "concentration", "minimal", "focus"],
    "Romantic": ["love", "romance", "smooth", "r&b", "soul"],
    "Nostalgic": ["80s", "90s", "oldies", "classic", "retro"],
    "Excited": ["party", "edm", "dance", "upbeat", "pop"],
    "Sleepy": ["sleep", "ambient", "lullaby", "soft", "quiet"],
    "Angry": ["metal", "hard rock", "punk", "aggressive", "intense"]
}

# Favorite artists (user priorities)
FAVORITE_ARTISTS = {
    "Taylor Swift": "06HL4z0CvFAxyc27GXpf02",
    "Selena Gomez": "0C8ZW7ezQVs4URX5aX7Kqx",
    "Ed Sheeran": "6eUKZXaKkcviH0Ku9w2n3V",
    "Justin Bieber": "1uNFoZAHBGtllmzznpCI3s", 
    "Alan Walker": "7vk5e3vY1uw9plTHJAMwjN",
    "The Weeknd": "1Xyo4u8uXC1ZmMpatF05PJ"
}

# Popular tracks from favorite artists
POPULAR_TRACKS = {
    "Taylor Swift": ["0V3wPSX9ygBnCm8psDIegu", "1BxfuPKGuaTgP7aM0Bbdwr"], # Cruel Summer, Blank Space
    "Selena Gomez": ["7FIWs0pqAYbP91WWM0vlTQ", "2dpaYNEQHiRxtZbfNsse99"], # Calm Down, Love You Like a Love Song
    "Ed Sheeran": ["0V3wPSX9ygBnCm8psDIegu", "6PQ88X9TkUIAUIZJHW2upE"], # Shape of You, Perfect
    "Justin Bieber": ["4iJyoBOLtHqaGxP12qzhQI", "50kpGaPAhYJ3sGmk6vplg0"], # Stay, Love Yourself
    "Alan Walker": ["60ynsPSSKe6O3sfMgJPn74", "5h8LXUIoHLgpXM8rLI5JUl"], # Faded, Alone
    "The Weeknd": ["2p8IUWQDrpjuFltbdgLOag", "5Odq8ohlgIbQKMZivbWkEo"] # Blinding Lights, Save Your Tears
}

# Map moods to Spotify genres and seeds
MOOD_TO_SPOTIFY_SEEDS = {
    "Happy": {
        "genres": ["pop", "happy", "disco"],
        "artists": [FAVORITE_ARTISTS["Taylor Swift"], FAVORITE_ARTISTS["Ed Sheeran"]], 
        "tracks": [POPULAR_TRACKS["Taylor Swift"][0], POPULAR_TRACKS["Ed Sheeran"][0]]
    },
    "Energetic": {
        "genres": ["electronic", "dance", "edm"],
        "artists": [FAVORITE_ARTISTS["Alan Walker"], FAVORITE_ARTISTS["The Weeknd"]], 
        "tracks": [POPULAR_TRACKS["Alan Walker"][0], POPULAR_TRACKS["The Weeknd"][0]]
    },
    "Relaxed": {
        "genres": ["chill", "ambient", "acoustic"],
        "artists": [FAVORITE_ARTISTS["Ed Sheeran"], FAVORITE_ARTISTS["Taylor Swift"]], 
        "tracks": [POPULAR_TRACKS["Ed Sheeran"][1], POPULAR_TRACKS["Taylor Swift"][1]]
    },
    "Calm": {
        "genres": ["classical", "piano", "instrumental"],
        "artists": [FAVORITE_ARTISTS["Ed Sheeran"], FAVORITE_ARTISTS["Selena Gomez"]], 
        "tracks": [POPULAR_TRACKS["Ed Sheeran"][1], POPULAR_TRACKS["Selena Gomez"][1]]
    },
    "Sad": {
        "genres": ["sad", "blues", "singer-songwriter"],
        "artists": [FAVORITE_ARTISTS["Taylor Swift"], FAVORITE_ARTISTS["The Weeknd"]], 
        "tracks": [POPULAR_TRACKS["Taylor Swift"][1], POPULAR_TRACKS["The Weeknd"][1]]
    },
    "Anxious": {
        "genres": ["alternative", "indie", "experimental"],
        "artists": [FAVORITE_ARTISTS["The Weeknd"], FAVORITE_ARTISTS["Alan Walker"]], 
        "tracks": [POPULAR_TRACKS["The Weeknd"][0], POPULAR_TRACKS["Alan Walker"][1]]
    },
    "Focused": {
        "genres": ["study", "focus", "instrumental"],
        "artists": [FAVORITE_ARTISTS["Ed Sheeran"], FAVORITE_ARTISTS["Alan Walker"]], 
        "tracks": [POPULAR_TRACKS["Ed Sheeran"][1], POPULAR_TRACKS["Alan Walker"][1]]
    },
    "Romantic": {
        "genres": ["r-n-b", "love", "soul"],
        "artists": [FAVORITE_ARTISTS["Justin Bieber"], FAVORITE_ARTISTS["Selena Gomez"]], 
        "tracks": [POPULAR_TRACKS["Justin Bieber"][1], POPULAR_TRACKS["Selena Gomez"][1]]
    },
    "Nostalgic": {
        "genres": ["80s", "90s", "pop"],
        "artists": [FAVORITE_ARTISTS["Taylor Swift"], FAVORITE_ARTISTS["Justin Bieber"]], 
        "tracks": [POPULAR_TRACKS["Taylor Swift"][1], POPULAR_TRACKS["Justin Bieber"][1]]
    },
    "Excited": {
        "genres": ["party", "edm", "dance"],
        "artists": [FAVORITE_ARTISTS["Justin Bieber"], FAVORITE_ARTISTS["Selena Gomez"]], 
        "tracks": [POPULAR_TRACKS["Justin Bieber"][0], POPULAR_TRACKS["Selena Gomez"][0]]
    },
    "Sleepy": {
        "genres": ["sleep", "ambient", "meditation"],
        "artists": [FAVORITE_ARTISTS["Ed Sheeran"], FAVORITE_ARTISTS["Taylor Swift"]], 
        "tracks": [POPULAR_TRACKS["Ed Sheeran"][1], POPULAR_TRACKS["Taylor Swift"][1]]
    },
    "Angry": {
        "genres": ["electronic", "dance", "pop-rock"],
        "artists": [FAVORITE_ARTISTS["Alan Walker"], FAVORITE_ARTISTS["The Weeknd"]], 
        "tracks": [POPULAR_TRACKS["Alan Walker"][1], POPULAR_TRACKS["The Weeknd"][0]]
    }
}

# Initialize Spotify client
def get_spotify_client():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        raise ValueError("Spotify credentials not found in environment variables")
    
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, 
        client_secret=client_secret
    )
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Hardcoded backup songs for each mood (with emoji icons instead of images)
BACKUP_RECOMMENDATIONS = {
    "Happy": [
        {"name": "Cruel Summer", "artist": "Taylor Swift", "url": "https://open.spotify.com/track/1BxfuPKGuaTgP7aM0Bbdwr", 
         "emoji": "🎶"},
        {"name": "Shape of You", "artist": "Ed Sheeran", "url": "https://open.spotify.com/track/7qiZfU4dY1lWllzX7mPBI3", 
         "emoji": "🎧"},
        {"name": "Can't Stop the Feeling!", "artist": "Justin Timberlake", "url": "https://open.spotify.com/track/1WkMMavIMc4JZ8cfMmMvR3", 
         "emoji": "🔥"},
        {"name": "Good as Hell", "artist": "Lizzo", "url": "https://open.spotify.com/track/60nZcImufyMA1MKQY3dcCH", 
         "emoji": "😊"},
    ],
    "Energetic": [
        {"name": "Faded", "artist": "Alan Walker", "url": "https://open.spotify.com/track/60ynsPSSKe6O3sfMgJPn74", 
         "emoji": "⚡"},
        {"name": "Blinding Lights", "artist": "The Weeknd", "url": "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b", 
         "emoji": "💡"},
        {"name": "Stay", "artist": "Justin Bieber", "url": "https://open.spotify.com/track/5HCyWlXZPP0y6Gqq8TgA20", 
         "emoji": "🎼"},
        {"name": "Don't Start Now", "artist": "Dua Lipa", "url": "https://open.spotify.com/track/3PfIrDoz19wz7qK7tYeu62", 
         "emoji": "💃"},
    ],
    "Relaxed": [
        {"name": "Perfect", "artist": "Ed Sheeran", "url": "https://open.spotify.com/track/0tgVpDi06FyKpA1z0VMD4v", 
         "emoji": "🎸"},
        {"name": "cardigan", "artist": "Taylor Swift", "url": "https://open.spotify.com/track/4R2kfaDFhslZEMJqAFNpdd", 
         "emoji": "🧣"},
        {"name": "Wolves", "artist": "Selena Gomez", "url": "https://open.spotify.com/track/0tBbt8CrmxbjRP0pueQkyU", 
         "emoji": "🎵"},
        {"name": "Sunflower", "artist": "Post Malone, Swae Lee", "url": "https://open.spotify.com/track/3KkXRkHbMCARz0aVfEt68P", 
         "emoji": "🌻"},
    ],
    "Calm": [
        {"name": "River Flows In You", "artist": "Yiruma", "url": "https://open.spotify.com/track/36orMWv8bDQOZY8eCl9Z3p", 
         "emoji": "🌊"},
        {"name": "Experience", "artist": "Ludovico Einaudi", "url": "https://open.spotify.com/track/1BncfTJAWxrsxyT9culBrj", 
         "emoji": "🎹"},
        {"name": "Photograph", "artist": "Ed Sheeran", "url": "https://open.spotify.com/track/6fxVffaTuwjgEk5h9QyRjy", 
         "emoji": "📷"},
        {"name": "A Sky Full of Stars", "artist": "Coldplay", "url": "https://open.spotify.com/track/0FDzzruyVECATHXKHFs9eJ", 
         "emoji": "✨"},
    ],
    "Sad": [
        {"name": "All Too Well", "artist": "Taylor Swift", "url": "https://open.spotify.com/track/4OAuvHryIVv4kMDNSLuPt6", 
         "emoji": "😢"},
        {"name": "Glimpse of Us", "artist": "Joji", "url": "https://open.spotify.com/track/4MJKGuCeZVm3I7yv5b3rUu", 
         "emoji": "😔"},
        {"name": "Save Your Tears", "artist": "The Weeknd", "url": "https://open.spotify.com/track/2BcMwX1MPV6ZHP4tUT9uq6", 
         "emoji": "💧"},
        {"name": "When I Was Your Man", "artist": "Bruno Mars", "url": "https://open.spotify.com/track/0nJW01T7XtvILxQgC5J7Wh", 
         "emoji": "😓"},
    ],
    "Anxious": [
        {"name": "Stressed Out", "artist": "Twenty One Pilots", "url": "https://open.spotify.com/track/3CRDbSIZ4r5MsZ0YwxuEkn", 
         "emoji": "😰"},
        {"name": "The Hills", "artist": "The Weeknd", "url": "https://open.spotify.com/track/7fBv7CLKzipRk6EC6TWHOB", 
         "emoji": "🏔"},
        {"name": "Alone", "artist": "Alan Walker", "url": "https://open.spotify.com/track/0JiVRyTJcJAfoe2drkPL4J", 
         "emoji": "👻"},
        {"name": "The Middle", "artist": "Zedd, Maren Morris", "url": "https://open.spotify.com/track/09IStsImFySgyp0pIQdqAc", 
         "emoji": "⏱"},
    ],
    "Focused": [
        {"name": "Lo-fi hip hop mix", "artist": "Lofi Girl", "url": "https://open.spotify.com/track/0bXpmJyHHYPk6QBFj25bYF", 
         "emoji": "💻"},
        {"name": "The Scientist", "artist": "Coldplay", "url": "https://open.spotify.com/track/75JFxkI2RXiU7L9VXzMkle", 
         "emoji": "🧪"},
        {"name": "Thinking Out Loud", "artist": "Ed Sheeran", "url": "https://open.spotify.com/track/1Slwb6dOYkBlWal1PGtnNg", 
         "emoji": "🧠"},
        {"name": "Time", "artist": "Hans Zimmer", "url": "https://open.spotify.com/track/6fxVffaTuwjgEk5h9QyRjy", 
         "emoji": "⏰"},
    ],
    "Romantic": [
        {"name": "Love Story", "artist": "Taylor Swift", "url": "https://open.spotify.com/track/1vrd6UOGamcKNGnSHJQlSt", 
         "emoji": "❤️"},
        {"name": "Love Yourself", "artist": "Justin Bieber", "url": "https://open.spotify.com/track/1f8zcJPvJKvxAOjEqM7kgV", 
         "emoji": "💕"},
        {"name": "Lover", "artist": "Taylor Swift", "url": "https://open.spotify.com/track/1dGr1c8CrMLDpV6mPbImSI", 
         "emoji": "💞"},
        {"name": "Love You Like a Love Song", "artist": "Selena Gomez", "url": "https://open.spotify.com/track/1QV6tiMFM6fSOKOGLMHYYg", 
         "emoji": "🎤"},
    ],
    "Nostalgic": [
        {"name": "Blank Space", "artist": "Taylor Swift", "url": "https://open.spotify.com/track/1p80LdxRV74UKvL8gnD7ky", 
         "emoji": "🕰️"},
        {"name": "Sorry", "artist": "Justin Bieber", "url": "https://open.spotify.com/track/5v6ACdW3YQ9lxCRxNgL4y4", 
         "emoji": "📱"},
        {"name": "Dancing Queen", "artist": "ABBA", "url": "https://open.spotify.com/track/0GjEhVFGZW8afUYGChu3Rr", 
         "emoji": "👸"},
        {"name": "I Want It That Way", "artist": "Backstreet Boys", "url": "https://open.spotify.com/track/47BBI51FKFwOMlIiX6m8ya", 
         "emoji": "🔙"},
    ],
    "Excited": [
        {"name": "Calm Down", "artist": "Selena Gomez, Rema", "url": "https://open.spotify.com/track/7FIWs0pqAYbP91WWM0vlTQ", 
         "emoji": "🤩"},
        {"name": "What Do You Mean?", "artist": "Justin Bieber", "url": "https://open.spotify.com/track/3pzjHKrQSvXGHQ98dx18HI", 
         "emoji": "🤯"},
        {"name": "Don't Stop The Music", "artist": "Rihanna", "url": "https://open.spotify.com/track/0ByMNEPAPpOR5H69DVrTNy", 
         "emoji": "🕺"},
        {"name": "Forever", "artist": "Justin Bieber", "url": "https://open.spotify.com/track/3AJwUDP919kvQ9QcozQPxg", 
         "emoji": "🌟"},
    ],
    "Sleepy": [
        {"name": "May It Be", "artist": "Enya", "url": "https://open.spotify.com/track/6aBUnkXuCEQQHAlTokv9or", 
         "emoji": "🌙"},
        {"name": "Sleep On The Floor", "artist": "The Lumineers", "url": "https://open.spotify.com/track/0JezO4hdPUOhIy7gxQiCG9", 
         "emoji": "💤"},
        {"name": "Clair de Lune", "artist": "Claude Debussy", "url": "https://open.spotify.com/track/2cnGAVVEIg3GtxQ0I0jOdr", 
         "emoji": "🌌"},
        {"name": "Breathe", "artist": "Lauv", "url": "https://open.spotify.com/track/2cC6ackPBvUKatW9yOt57X", 
         "emoji": "😴"},
    ],
    "Angry": [
        {"name": "In The End", "artist": "Linkin Park", "url": "https://open.spotify.com/track/60a0Rd6pjrkxjPbaKzXjfq", 
         "emoji": "😠"},
        {"name": "Look What You Made Me Do", "artist": "Taylor Swift", "url": "https://open.spotify.com/track/1P17dC1amhFzptugyAO7Il", 
         "emoji": "😡"},
        {"name": "The Sound of Silence", "artist": "Disturbed", "url": "https://open.spotify.com/track/1Uj0QBaJZOb3m43xJ3VWoR", 
         "emoji": "🔇"},
        {"name": "bad guy", "artist": "Billie Eilish", "url": "https://open.spotify.com/track/2Fxmhks0bxGSBdJ92vM42m", 
         "emoji": "😈"},
    ]
}

def get_music_recommendations(mood: str, limit: int = 9) -> List[Dict[str, Any]]:
    """
    Get music recommendations based on the detected mood using Spotify API or fallback to hard-coded options.
    
    Args:
        mood: A string representing the user's mood.
        limit: Number of recommendations to return.
        
    Returns:
        A list of dictionaries containing music recommendations.
    """
    try:
        # Get Spotify client
        sp = get_spotify_client()
        
        # Default to Relaxed if mood not found
        if mood not in MOOD_TO_SPOTIFY_SEEDS:
            mood = "Relaxed"
        
        # Get seed values for the mood
        seed_data = MOOD_TO_SPOTIFY_SEEDS[mood]
        
        # Use simplified approach to avoid API errors
        seed_artists = random.sample(seed_data["artists"], min(2, len(seed_data["artists"])))
        seed_tracks = random.sample(seed_data["tracks"], min(3, len(seed_data["tracks"])))
        
        # Get recommendations from Spotify
        results = sp.recommendations(
            seed_artists=seed_artists,
            seed_tracks=seed_tracks,
            limit=limit
        )
        
        # Format the recommendations
        recommendations = []
        for track in results["tracks"]:
            # Get the album image if available
            image_url = None
            if track["album"]["images"] and len(track["album"]["images"]) > 0:
                # Get medium-sized image if available, otherwise use the first one
                if len(track["album"]["images"]) > 1:
                    image_url = track["album"]["images"][1]["url"]
                else:
                    image_url = track["album"]["images"][0]["url"]
            
            # Get the artist name
            artist_name = track["artists"][0]["name"] if track["artists"] else "Unknown Artist"
            
            # Create a recommendation item
            recommendations.append({
                "name": track["name"],
                "artist": artist_name,
                "url": track["external_urls"]["spotify"] if "external_urls" in track and "spotify" in track["external_urls"] else "",
                "image_url": image_url,
                "preview_url": track.get("preview_url", None)
            })
        
        return recommendations
    
    except Exception as e:
        # Log the error for debugging
        error_msg = f"Error fetching music recommendations: {str(e)}"
        print(error_msg)
        print(f"Using backup recommendations for mood: {mood}")
        
        # Use our hardcoded backup recommendations instead
        backup_recs = BACKUP_RECOMMENDATIONS.get(mood, BACKUP_RECOMMENDATIONS["Relaxed"])
        
        # Randomly shuffle and limit
        random.shuffle(backup_recs)
        return backup_recs[:limit]
