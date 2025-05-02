import requests
import random
from typing import List, Dict, Any

# Define mood to genre/tag mappings
MOOD_MAPPINGS = {
    "Happy": ["pop", "happy", "feel good", "upbeat", "cheerful"],
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

def get_music_recommendations(mood: str, limit: int = 9) -> List[Dict[str, Any]]:
    """
    Get music recommendations based on the detected mood using Last.fm API.
    
    Args:
        mood: A string representing the user's mood.
        limit: Number of recommendations to return.
        
    Returns:
        A list of dictionaries containing music recommendations.
    """
    # Get tags related to the mood
    if mood not in MOOD_MAPPINGS:
        mood = "Relaxed"  # Default to relaxed if mood is not found
    
    tags = MOOD_MAPPINGS[mood]
    
    # Randomly select two tags for variety
    selected_tags = random.sample(tags, min(2, len(tags)))
    tag_string = ",".join(selected_tags)
    
    # Last.fm API endpoint and parameters
    url = "https://ws.audioscrobbler.com/2.0/"
    
    # API parameters
    params = {
        "method": "tag.gettoptracks",
        "tag": tag_string,
        "api_key": "a0a150c8ac3069e94e9cc6d37ef41f29",  # This is a public API key for Last.fm
        "format": "json",
        "limit": 50  # Get 50 tracks, then we'll sample from them
    }
    
    try:
        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        data = response.json()
        
        # Extract track information
        tracks = data.get("tracks", {}).get("track", [])
        
        if not tracks:
            # Fallback to a different API method if no tracks found
            params["method"] = "tag.gettoptracks"
            params["tag"] = selected_tags[0] if selected_tags else "chill"
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            tracks = data.get("tracks", {}).get("track", [])
        
        # Randomly select a subset of tracks
        if len(tracks) > limit:
            tracks = random.sample(tracks, limit)
        
        # Format the recommendations
        recommendations = []
        for track in tracks:
            # Extract the medium-sized image URL if available
            image_url = None
            if "image" in track:
                for img in track["image"]:
                    if img["size"] == "medium" and "#text" in img and img["#text"]:
                        image_url = img["#text"]
                        break
            
            recommendations.append({
                "name": track.get("name", "Unknown Track"),
                "artist": track.get("artist", {}).get("name", "Unknown Artist"),
                "url": track.get("url", ""),
                "image_url": image_url
            })
        
        return recommendations
    
    except requests.RequestException as e:
        # Log the error for debugging
        print(f"Error fetching music recommendations: {str(e)}")
        
        # Return an empty list in case of error
        return []
