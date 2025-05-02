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
    """Create and return a Spotify client using environment variables."""
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        raise ValueError("Spotify credentials not found in environment variables")
    
    # Avoid cache issues
    auth_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret,
        cache_handler=None
    )
    
    return spotipy.Spotify(
        auth_manager=auth_manager,
        requests_timeout=20
    )

def search_tracks_by_artist_and_keyword(sp, artist_name: str, keyword: str, limit: int = 9):
    """Search for tracks by artist name and keyword."""
    try:
        # Create a search query
        search_query = f"artist:{artist_name} {keyword}"
        print(f"Searching with query: {search_query}")
        
        # Execute the search
        results = sp.search(q=search_query, type="track", limit=limit)
        return results["tracks"]["items"]
    except Exception as e:
        print(f"Search error: {str(e)}")
        return []

def format_track_data(tracks):
    """Format track data into a consistent structure."""
    recommendations = []
    
    for track in tracks:
        try:
            # Get the highest quality album image
            image_url = None
            if track["album"]["images"] and len(track["album"]["images"]) > 0:
                # Spotify returns images in order of size (largest first)
                # Get the largest image for best quality
                image_url = track["album"]["images"][0]["url"]
                print(f"Found album image for '{track['name']}': {image_url}")
            else:
                print(f"No album image found for track: {track['name']}")
            
            # Get artist name
            artist_name = track["artists"][0]["name"] if track["artists"] else "Unknown Artist"
            
            # Create recommendation item
            recommendations.append({
                "name": track["name"],
                "artist": artist_name,
                "url": track["external_urls"]["spotify"] if "external_urls" in track and "spotify" in track["external_urls"] else "",
                "image_url": image_url,
                "preview_url": track.get("preview_url", None),
                "album_name": track["album"]["name"] if "album" in track else ""
            })
        except Exception as e:
            print(f"Error formatting track: {str(e)}")
    
    # Print a summary
    print(f"Formatted {len(recommendations)} tracks from Spotify")
    return recommendations

def get_music_recommendations(mood: str, limit: int = 15) -> List[Dict[str, Any]]:
    """Get music recommendations based on mood."""
    try:
        # Initialize Spotify client
        sp = get_spotify_client()
        
        # Default to Relaxed if mood not found
        if mood not in MOOD_TO_SPOTIFY_SEEDS:
            mood = "Relaxed"
        
        # Get seed data for the mood
        seed_data = MOOD_TO_SPOTIFY_SEEDS[mood]
        
        try:
            # Try using recommendations API first
            print(f"Getting recommendations for mood: {mood}")
            
            # Sample seeds - with fewer seeds to improve reliability
            seed_genres = random.sample(seed_data["genres"], min(1, len(seed_data["genres"])))
            seed_artists = random.sample(seed_data["artists"], min(1, len(seed_data["artists"])))
            seed_tracks = random.sample(seed_data["tracks"], min(1, len(seed_data["tracks"])))
            
            print(f"Seeds: artists={seed_artists}, tracks={seed_tracks}, genres={seed_genres}")
            
            # Get recommendations
            results = sp.recommendations(
                seed_artists=seed_artists,
                seed_tracks=seed_tracks,
                seed_genres=seed_genres,
                limit=limit
            )
            
            if "tracks" in results and results["tracks"]:
                return format_track_data(results["tracks"])
            else:
                raise Exception("No tracks returned from recommendations API")
                
        except Exception as rec_error:
            # If recommendations API fails, use search fallback
            print(f"Recommendation API error: {str(rec_error)}")
            print("Falling back to direct search...")
            
            # Choose an artist to search
            artist_name = random.choice(list(FAVORITE_ARTISTS.keys()))
            keyword = random.choice(MOOD_MAPPINGS[mood])
            
            # Search for tracks
            tracks = search_tracks_by_artist_and_keyword(sp, artist_name, keyword, limit)
            
            if tracks:
                return format_track_data(tracks)
            else:
                print("Search returned no results, trying one more artist...")
                
                # Try with a different artist
                artist_name = random.choice([a for a in list(FAVORITE_ARTISTS.keys()) if a != artist_name])
                tracks = search_tracks_by_artist_and_keyword(sp, artist_name, keyword, limit)
                
                if tracks:
                    return format_track_data(tracks)
    
    except Exception as e:
        print(f"Error getting music recommendations: {str(e)}")
    
    # Return some sample data in case all else fails
    print("All recommendation methods failed, returning empty list")
    return []
