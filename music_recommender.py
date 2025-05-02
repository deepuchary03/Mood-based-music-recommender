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

# Map moods to Spotify genres and seeds
MOOD_TO_SPOTIFY_SEEDS = {
    "Happy": {
        "genres": ["pop", "happy", "disco"],
        "artists": ["4gzpq5DPGxSnKTe4SA8HAU", "6sFIWsNpZYqfjUpaCgueju"], # Coldplay, Adele
        "tracks": ["6DCZcSspjsKoFjzjrWoCdn", "60nZcImufyMA1MKQY3dcCH"] # Happy - Pharrell, Good as Hell - Lizzo
    },
    "Energetic": {
        "genres": ["electronic", "dance", "edm"],
        "artists": ["4YRxDV8wJFPHPTeXepOstw", "23fqKkggKUBHNkbKtXEls4"], # Avicii, Kygo
        "tracks": ["2KH16WveTQWT6KOG9Rg6e2", "6Xgq7MvZiet0hVi3KaDSgJ"] # Titanium, Uptown Funk
    },
    "Relaxed": {
        "genres": ["chill", "ambient", "acoustic"],
        "artists": ["6eUKZXaKkcviH0Ku9w2n3V", "00FQb4jTyendYWaN8pK0wa"], # Ed Sheeran, Lana Del Rey
        "tracks": ["0rKtyWc8bvkriBthvHKY8d", "0GLyymAV86KIVUYJzRyJIR"] # River Flows in You, Experience
    },
    "Calm": {
        "genres": ["classical", "piano", "instrumental"],
        "artists": ["2wOqMjp9TyABvtHdOSOTUS", "0X2BH1fck6amBIoJhDVmmJ"], # Ludovico Einaudi, Elijah Woods
        "tracks": ["0YwBZKT0PELZyWw1HA0Kw9", "6vFsBXYczYsP0H1rA7kvV5"] # Nuvole Bianche, Clair de Lune
    },
    "Sad": {
        "genres": ["sad", "blues", "singer-songwriter"],
        "artists": ["5pKCCKE2ajJHZ9KAiaK11H", "06HL4z0CvFAxyc27GXpf02"], # Radiohead, Taylor Swift
        "tracks": ["1lzr43nnXAijIGYnCT8M8H", "4h9wh7iOZ0GGn8QVp4RAOB"] # Creep, All Too Well
    },
    "Anxious": {
        "genres": ["alternative", "indie", "experimental"],
        "artists": ["53XhwfbYqKCa1cC15pYq2q", "0k17h0D3J5VfsdmQ1iZtE9"], # Metallica, Pink Floyd
        "tracks": ["7ouMYWpwJ422jRcDASZB7P", "2CgOd0Lj5MuvOqzqdaAXtS"] # One, Money
    },
    "Focused": {
        "genres": ["study", "focus", "instrumental"],
        "artists": ["2wOqMjp9TyABvtHdOSOTUS", "0Xk15jHKly4c3AhPr5vjoA"], # Ludovico Einaudi, Hans Zimmer
        "tracks": ["6fxVffaTuwjgEk5h9QyRjy", "2RSHsoi04658QL5xgQVov3"] # Time, Interstellar Theme
    },
    "Romantic": {
        "genres": ["r-n-b", "love", "soul"],
        "artists": ["3TVXtAsR1Inumwj472S9r4", "5ZsFI1h6hIdQRw2ti0hz81"], # Drake, ZAYN
        "tracks": ["0VjIjW4GlUZAMYd2vXMi3b", "14iI3HO9P4X6xs6lBZctHe"] # Thinking Out Loud, Pillowtalk
    },
    "Nostalgic": {
        "genres": ["80s", "90s", "oldies"],
        "artists": ["0oSGxfWSnnOXhD2fKuz2Gy", "1dfeR4HaWDbWqFHLkxsg1d"], # Abba, Queen
        "tracks": ["4NsPgRYUdHu2Q5JRNgXYU5", "5vdp5UmvTsnMEMESIF2Ym7"] # Dancing Queen, Another One Bites the Dust
    },
    "Excited": {
        "genres": ["party", "edm", "dance"],
        "artists": ["64KEffDW9EtZ1y2vBYgq8T", "1uNFoZAHBGtllmzznpCI3s"], # Marshmello, Justin Bieber
        "tracks": ["5jnxScfRVyWskdfPGjTF7c", "60nZcImufyMA1MKQY3dcCH"] # Don't Stop the Music, Good as Hell
    },
    "Sleepy": {
        "genres": ["sleep", "ambient", "meditation"],
        "artists": ["4NHQUGzhtTLFvgF5SZesLK", "5IH6FPUwQTxPSXurCrcIov"], # Enya, Explosions in the Sky
        "tracks": ["2EEeorm0jyVX4LT0zRXHaD", "6vFsBXYczYsP0H1rA7kvV5"] # May It Be, Clair de Lune
    },
    "Angry": {
        "genres": ["metal", "hard-rock", "punk-rock"],
        "artists": ["7jy3rLJdDQY21OgRLCZ9sD", "6XyY86QOPPrYVGvF9ch6wz"], # Linkin Park, Disturbed
        "tracks": ["60a0Rd6pjrkxjPbaKzXjfq", "2MuWTIM3b0YEAskbeeFE1i"] # In The End, The Sound of Silence (Disturbed)
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

def get_music_recommendations(mood: str, limit: int = 9) -> List[Dict[str, Any]]:
    """
    Get music recommendations based on the detected mood using Spotify API.
    
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
        
        # Take a random sample of seeds to use (Spotify API accepts up to 5 seeds total)
        seed_genres = random.sample(seed_data["genres"], min(2, len(seed_data["genres"])))
        seed_artists = random.sample(seed_data["artists"], min(1, len(seed_data["artists"])))
        seed_tracks = random.sample(seed_data["tracks"], min(2, len(seed_data["tracks"])))
        
        # Get recommendations from Spotify
        results = sp.recommendations(
            seed_genres=seed_genres,
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
        print(f"Error fetching music recommendations: {str(e)}")
        
        # Return an empty list in case of error
        return []
