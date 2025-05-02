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

# Hardcoded backup songs for each mood
BACKUP_RECOMMENDATIONS = {
    "Happy": [
        {"name": "Cruel Summer", "artist": "Taylor Swift", "url": "https://open.spotify.com/track/1BxfuPKGuaTgP7aM0Bbdwr", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273e787cffec20aa2a396a61647"},
        {"name": "Shape of You", "artist": "Ed Sheeran", "url": "https://open.spotify.com/track/7qiZfU4dY1lWllzX7mPBI3", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273ba5db46f4b838ef6027e6f96"},
        {"name": "Can't Stop the Feeling!", "artist": "Justin Timberlake", "url": "https://open.spotify.com/track/1WkMMavIMc4JZ8cfMmMvR3", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273150bd92ac0a3403b11c5c538"},
        {"name": "Good as Hell", "artist": "Lizzo", "url": "https://open.spotify.com/track/60nZcImufyMA1MKQY3dcCH", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273c9824a247d586c9f9eff5c6f"},
        {"name": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars", "url": "https://open.spotify.com/track/32OlwWuMpZ6b0aN2RZOeMS", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2732c3bd069ae0ed17899e4d9a8"},
    ],
    "Energetic": [
        {"name": "Faded", "artist": "Alan Walker", "url": "https://open.spotify.com/track/60ynsPSSKe6O3sfMgJPn74", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2738451706cb6398f64f460c10a"},
        {"name": "Blinding Lights", "artist": "The Weeknd", "url": "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2738863bc11d2aa12b54f5aeb36"},
        {"name": "Stay", "artist": "Justin Bieber", "url": "https://open.spotify.com/track/5HCyWlXZPP0y6Gqq8TgA20", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2739e00bbf49aff7b18983f2290"},
        {"name": "Don't Start Now", "artist": "Dua Lipa", "url": "https://open.spotify.com/track/3PfIrDoz19wz7qK7tYeu62", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273bd26ede1ae69327010d49946"},
    ],
    "Relaxed": [
        {"name": "Perfect", "artist": "Ed Sheeran", "url": "https://open.spotify.com/track/0tgVpDi06FyKpA1z0VMD4v", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273ba5db46f4b838ef6027e6f96"},
        {"name": "cardigan", "artist": "Taylor Swift", "url": "https://open.spotify.com/track/4R2kfaDFhslZEMJqAFNpdd", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273c288028c2592f400dd0b9233"},
        {"name": "Wolves", "artist": "Selena Gomez", "url": "https://open.spotify.com/track/0tBbt8CrmxbjRP0pueQkyU", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2736ef76a0f37557bf385fe76c1"},
        {"name": "Sunflower", "artist": "Post Malone, Swae Lee", "url": "https://open.spotify.com/track/3KkXRkHbMCARz0aVfEt68P", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2739478c87599550dd73bfa7e02"},
    ],
    "Calm": [
        {"name": "River Flows In You", "artist": "Yiruma", "url": "https://open.spotify.com/track/36orMWv8bDQOZY8eCl9Z3p", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273e300e3fa239a6f40f9c18449"},
        {"name": "Experience", "artist": "Ludovico Einaudi", "url": "https://open.spotify.com/track/1BncfTJAWxrsxyT9culBrj", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273e0d49f0fa21f5f560f87c925"},
        {"name": "Photograph", "artist": "Ed Sheeran", "url": "https://open.spotify.com/track/6fxVffaTuwjgEk5h9QyRjy", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2735a8e97f5d6a2bd198c643e89"},
        {"name": "A Sky Full of Stars", "artist": "Coldplay", "url": "https://open.spotify.com/track/0FDzzruyVECATHXKHFs9eJ", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2734e19d0ad7a5302b0a70efcb8"},
    ],
    "Sad": [
        {"name": "All Too Well", "artist": "Taylor Swift", "url": "https://open.spotify.com/track/4OAuvHryIVv4kMDNSLuPt6", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273318443aab3531a7d5cc552d1"},
        {"name": "Glimpse of Us", "artist": "Joji", "url": "https://open.spotify.com/track/4MJKGuCeZVm3I7yv5b3rUu", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2731492e6f7fa56befa09ef8cfb"},
        {"name": "Save Your Tears", "artist": "The Weeknd", "url": "https://open.spotify.com/track/2BcMwX1MPV6ZHP4tUT9uq6", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2738863bc11d2aa12b54f5aeb36"},
        {"name": "When I Was Your Man", "artist": "Bruno Mars", "url": "https://open.spotify.com/track/0nJW01T7XtvILxQgC5J7Wh", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2738c5b37fc90d1d4773474e8d1"},
    ],
    "Anxious": [
        {"name": "Stressed Out", "artist": "Twenty One Pilots", "url": "https://open.spotify.com/track/3CRDbSIZ4r5MsZ0YwxuEkn", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2734d9f7a88a7979c3e0720cea5"},
        {"name": "The Hills", "artist": "The Weeknd", "url": "https://open.spotify.com/track/7fBv7CLKzipRk6EC6TWHOB", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2733daf2975e11555b423147592"},
        {"name": "Alone", "artist": "Alan Walker", "url": "https://open.spotify.com/track/0JiVRyTJcJAfoe2drkPL4J", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273c7aaa0ed5df66031b6d8a156"},
        {"name": "The Middle", "artist": "Zedd, Maren Morris", "url": "https://open.spotify.com/track/09IStsImFySgyp0pIQdqAc", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2736087fe81cd6fa398e6d90aa7"},
    ],
    "Focused": [
        {"name": "Lo-fi hip hop mix", "artist": "Lofi Girl", "url": "https://open.spotify.com/track/0bXpmJyHHYPk6QBFj25bYF", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273e4c6c4347d3d8e4e58f638c7"},
        {"name": "The Scientist", "artist": "Coldplay", "url": "https://open.spotify.com/track/75JFxkI2RXiU7L9VXzMkle", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2736d3206b6e521139eee2cebf5"},
        {"name": "Thinking Out Loud", "artist": "Ed Sheeran", "url": "https://open.spotify.com/track/1Slwb6dOYkBlWal1PGtnNg", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2735a8e97f5d6a2bd198c643e89"},
        {"name": "Time", "artist": "Hans Zimmer", "url": "https://open.spotify.com/track/6fxVffaTuwjgEk5h9QyRjy", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b27318d3e27da112297eea45714b"},
    ],
    "Romantic": [
        {"name": "Love Story", "artist": "Taylor Swift", "url": "https://open.spotify.com/track/1vrd6UOGamcKNGnSHJQlSt", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2732a5ef0679c8c6315dc69de44"},
        {"name": "Love Yourself", "artist": "Justin Bieber", "url": "https://open.spotify.com/track/1f8zcJPvJKvxAOjEqM7kgV", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2739513d193cbd138a179425a2a"},
        {"name": "Lover", "artist": "Taylor Swift", "url": "https://open.spotify.com/track/1dGr1c8CrMLDpV6mPbImSI", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273e787cffec20aa2a396a61647"},
        {"name": "Love You Like a Love Song", "artist": "Selena Gomez", "url": "https://open.spotify.com/track/1QV6tiMFM6fSOKOGLMHYYg", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273b571ca5253c4e85cfa446b5d"},
    ],
    "Nostalgic": [
        {"name": "Blank Space", "artist": "Taylor Swift", "url": "https://open.spotify.com/track/1p80LdxRV74UKvL8gnD7ky", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2739abdf14e6058bd3903686148"},
        {"name": "Sorry", "artist": "Justin Bieber", "url": "https://open.spotify.com/track/5v6ACdW3YQ9lxCRxNgL4y4", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2739513d193cbd138a179425a2a"},
        {"name": "Dancing Queen", "artist": "ABBA", "url": "https://open.spotify.com/track/0GjEhVFGZW8afUYGChu3Rr", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2733d92b2ad5af9fbc8637425f0"},
        {"name": "I Want It That Way", "artist": "Backstreet Boys", "url": "https://open.spotify.com/track/47BBI51FKFwOMlIiX6m8ya", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273cf8a38c4cad5185725b39859"},
    ],
    "Excited": [
        {"name": "Calm Down", "artist": "Selena Gomez, Rema", "url": "https://open.spotify.com/track/7FIWs0pqAYbP91WWM0vlTQ", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273e0de1a04b5fa6ddf4c218a15"},
        {"name": "What Do You Mean?", "artist": "Justin Bieber", "url": "https://open.spotify.com/track/3pzjHKrQSvXGHQ98dx18HI", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2739513d193cbd138a179425a2a"},
        {"name": "Don't Stop The Music", "artist": "Rihanna", "url": "https://open.spotify.com/track/0ByMNEPAPpOR5H69DVrTNy", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273c9aab45d55a3e5d034eda561"},
        {"name": "Forever", "artist": "Justin Bieber", "url": "https://open.spotify.com/track/3AJwUDP919kvQ9QcozQPxg", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2739513d193cbd138a179425a2a"},
    ],
    "Sleepy": [
        {"name": "May It Be", "artist": "Enya", "url": "https://open.spotify.com/track/6aBUnkXuCEQQHAlTokv9or", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273a0c61b4efddd3f38afa953ab"},
        {"name": "Sleep On The Floor", "artist": "The Lumineers", "url": "https://open.spotify.com/track/0JezO4hdPUOhIy7gxQiCG9", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2731bd4c8844907a65b38888a17"},
        {"name": "Clair de Lune", "artist": "Claude Debussy", "url": "https://open.spotify.com/track/2cnGAVVEIg3GtxQ0I0jOdr", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273c96582a4422bbecb9f466b99"},
        {"name": "Breathe", "artist": "Lauv", "url": "https://open.spotify.com/track/2cC6ackPBvUKatW9yOt57X", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b27352adae9191743520b59a095d"},
    ],
    "Angry": [
        {"name": "In The End", "artist": "Linkin Park", "url": "https://open.spotify.com/track/60a0Rd6pjrkxjPbaKzXjfq", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273e2f039481babe23698bfa5e7"},
        {"name": "Look What You Made Me Do", "artist": "Taylor Swift", "url": "https://open.spotify.com/track/1P17dC1amhFzptugyAO7Il", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b27390fd9741e1838115cd90b3b6"},
        {"name": "The Sound of Silence", "artist": "Disturbed", "url": "https://open.spotify.com/track/1Uj0QBaJZOb3m43xJ3VWoR", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b2739b19c107109de740bad72df5"},
        {"name": "bad guy", "artist": "Billie Eilish", "url": "https://open.spotify.com/track/2Fxmhks0bxGSBdJ92vM42m", 
         "image_url": "https://i.scdn.co/image/ab67616d0000b273a91c10fe9472d9bd89802e5a"},
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
