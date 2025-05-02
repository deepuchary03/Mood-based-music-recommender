import requests
import random
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

# Map moods to Deezer genre IDs
MOOD_TO_DEEZER_GENRE = {
    "Happy": [132, 116, 165],  # Pop, Party, Disco
    "Energetic": [152, 113, 106],  # Rock, Dance, Electro
    "Relaxed": [98, 129, 75],  # Chill, Ambient, Acoustic
    "Calm": [98, 16, 84],  # Ambient, Classical, Piano
    "Sad": [153, 85, 169],  # Blues, Alternative, Soul & Funk
    "Anxious": [464, 85, 40],  # Electro, Alternative, Indie
    "Focused": [98, 84, 116],  # Ambient, Piano, Instrumental
    "Romantic": [169, 153, 116],  # Soul & Funk, Blues, R&B
    "Nostalgic": [466, 144, 98],  # Folk, 80s, Ambient
    "Excited": [113, 116, 106],  # Dance, Party, Electro
    "Sleepy": [98, 16, 84],  # Ambient, Classical, Piano 
    "Angry": [152, 464, 173]  # Rock, Metal, Punk
}

def get_music_recommendations(mood: str, limit: int = 9) -> List[Dict[str, Any]]:
    """
    Get music recommendations based on the detected mood using Deezer API.
    
    Args:
        mood: A string representing the user's mood.
        limit: Number of recommendations to return.
        
    Returns:
        A list of dictionaries containing music recommendations.
    """
    # Get genres related to the mood
    if mood not in MOOD_TO_DEEZER_GENRE:
        mood = "Relaxed"  # Default to relaxed if mood is not found
    
    # Get genre IDs for this mood
    genre_ids = MOOD_TO_DEEZER_GENRE[mood]
    
    # Randomly select one genre ID for variety
    selected_genre = random.choice(genre_ids)
    
    # Deezer API endpoint for chart tracks by genre
    url = f"https://api.deezer.com/chart/{selected_genre}/tracks"
    
    try:
        # Make the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        data = response.json()
        
        # Extract track information
        tracks = data.get("data", [])
        
        if not tracks and len(genre_ids) > 1:
            # Try a different genre if the first one didn't work
            backup_genres = [g for g in genre_ids if g != selected_genre]
            backup_genre = random.choice(backup_genres)
            backup_url = f"https://api.deezer.com/chart/{backup_genre}/tracks"
            
            response = requests.get(backup_url)
            response.raise_for_status()
            
            data = response.json()
            tracks = data.get("data", [])
        
        # If still no tracks, try a search with keyword from mood mappings
        if not tracks:
            keyword = random.choice(MOOD_MAPPINGS[mood])
            search_url = f"https://api.deezer.com/search?q={keyword}&limit=30"
            
            response = requests.get(search_url)
            response.raise_for_status()
            
            data = response.json()
            tracks = data.get("data", [])
        
        # Randomly select a subset of tracks
        if len(tracks) > limit:
            tracks = random.sample(tracks, limit)
        
        # Format the recommendations
        recommendations = []
        for track in tracks:
            # Get album image if available
            image_url = None
            if "album" in track and "cover_medium" in track["album"]:
                image_url = track["album"]["cover_medium"]
            
            recommendations.append({
                "name": track.get("title", "Unknown Track"),
                "artist": track.get("artist", {}).get("name", "Unknown Artist"),
                "url": track.get("link", ""),
                "image_url": image_url
            })
        
        return recommendations
    
    except requests.RequestException as e:
        # Log the error for debugging
        print(f"Error fetching music recommendations: {str(e)}")
        
        # Return an empty list in case of error
        return []
