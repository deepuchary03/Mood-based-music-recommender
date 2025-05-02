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
        
        # Use simplified approach to avoid API errors
        # Spotify allows maximum of 5 total seeds, so use 2 genres, 1 artist, and 2 tracks
        
        # Let's simplify and just use artists and tracks
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
        
        # For specific Spotify API errors, handle them differently
        if "http status: 401" in str(e) or "http status: 404" in str(e):
            print("Authentication error: Please check your Spotify API credentials")
            # Try a search instead as fallback
            try:
                # Try to search specifically for songs by favorite artists that match the mood
                favorite_artists = list(FAVORITE_ARTISTS.values())
                
                # Use one of the artist names and a mood keyword for a more focused search
                artist_name = random.choice(list(FAVORITE_ARTISTS.keys()))
                keyword = random.choice(MOOD_MAPPINGS[mood])
                
                # Perform search
                search_query = f"artist:{artist_name} {keyword}"
                print(f"Performing fallback search with query: {search_query}")
                results = sp.search(q=search_query, type="track", limit=limit)
                tracks = results["tracks"]["items"]
                
                recommendations = []
                for track in tracks:
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
            except Exception as inner_e:
                print(f"Fallback search also failed: {str(inner_e)}")
        
        # Return an empty list in case of error
        return []
