import streamlit as st
import os
from music_recommender import get_music_recommendations

# Set page configuration
st.set_page_config(
    page_title="Mood-Based Music Recommender",
    page_icon="🎵",
    layout="wide",
)

# Custom CSS
st.markdown("""
<style>
    .main {background-color: #f5f5f5;}
    .stApp {max-width: 1200px; margin: 0 auto;}
    h1 {color: #1DB954; text-align: center; margin-bottom: 0.5em;}
    .description {font-size: 1.2em; text-align: center; margin-bottom: 2em;}
    .stButton>button {background-color: #1DB954; color: white; border: none; padding: 0.5em 2em; border-radius: 30px;}
    .stButton>button:hover {background-color: #14943E;}
    div.stSelectbox > div > div > div {background-color: white; border-radius: 10px;}
    div.stSelectbox > div > div > div:hover {border-color: #1DB954;}
    .footer {text-align: center; margin-top: 2em; color: #555;}
    .st-bd {border-color: #1DB954 !important;}
</style>
""", unsafe_allow_html=True)

# App title and description with emoji - using native Streamlit functions
st.title("🎵 Mood-Based Music Recommender")
st.write("Get personalized music recommendations based on your current mood featuring your favorite artists!")

# Initialize session state variables if they don't exist
if 'detected_mood' not in st.session_state:
    st.session_state.detected_mood = None
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None

# Mood selection
st.header("Select Your Mood")

moods = [
    "Happy", "Energetic", "Relaxed", "Calm", 
    "Sad", "Anxious", "Focused", "Romantic",
    "Nostalgic", "Excited", "Sleepy", "Angry"
]

selected_mood = st.selectbox("Choose your current mood:", [""] + moods, index=0)

if st.button("Get Music Recommendations", type="primary"):
    if selected_mood:
        st.session_state.detected_mood = selected_mood
        with st.spinner(f"Finding music for your {selected_mood.lower()} mood..."):
            try:
                st.session_state.recommendations = get_music_recommendations(selected_mood)
                st.rerun()
            except Exception as e:
                st.error(f"Error getting recommendations: {str(e)}")
    else:
        st.warning("Please select a mood first!")

# Display results section
if st.session_state.detected_mood:
    st.markdown("<hr style='margin: 25px 0; height: 3px; background: linear-gradient(to right, #1DB954, #191414);'>", unsafe_allow_html=True)
    
    # Display detected mood with an emoji and styling
    mood_emojis = {
        "Happy": "😊", "Energetic": "⚡", "Relaxed": "😌", "Calm": "🧘",
        "Sad": "😢", "Anxious": "😰", "Focused": "🧠", "Romantic": "❤️",
        "Nostalgic": "🕰️", "Excited": "🤩", "Sleepy": "😴", "Angry": "😠"
    }
    
    mood = st.session_state.detected_mood
    emoji = mood_emojis.get(mood, "🎵")
    
    # Display mood header using Streamlit's native functions
    st.header(f"Your {mood} {emoji} Music")
    st.write("Featuring songs from your favorite artists")
    st.markdown("---")
    
    # Display recommendations
    if st.session_state.recommendations:
        if len(st.session_state.recommendations) > 0:
            # Create a grid layout for recommendations
            cols = st.columns(3)
            
            for i, track in enumerate(st.session_state.recommendations):
                with cols[i % 3]:
                    # Create a simple card with consistent styling
                    st.write(f"**{track['name']}**")
                    st.write(f"*{track['artist']}*")
                    
                    # Display image using st.image which is more reliable
                    if 'image_url' in track and track['image_url']:
                        try:
                            st.image(track['image_url'], width=180)
                        except Exception as e:
                            st.write("Image unavailable")
                    
                    # Add a preview player if available
                    if 'preview_url' in track and track['preview_url']:
                        st.audio(track['preview_url'], format='audio/mp3')
                    
                    # Add a link to listen to the track
                    if 'url' in track:
                        st.markdown(f"[Listen on Spotify]({track['url']})")
                    
                    st.markdown("---")
        else:
            st.info("No recommendations found for this mood. Try a different mood.")
    else:
        st.info("Recommendations will appear here once your mood is analyzed.")
        
    # Add an artist feature section
    st.markdown("---")
    st.header("Your Favorite Artists")
    
    # Simple emoji approach for artists (much more reliable than external images)
    artist_info = {
        "Taylor Swift": {
            "emoji": "👩‍🎤",
            "id": "06HL4z0CvFAxyc27GXpf02"
        },
        "Selena Gomez": {
            "emoji": "👩‍🎤", 
            "id": "0C8ZW7ezQVs4URX5aX7Kqx"
        },
        "Ed Sheeran": {
            "emoji": "👨‍🎤",
            "id": "6eUKZXaKkcviH0Ku9w2n3V"
        },
        "Justin Bieber": {
            "emoji": "👨‍🎤",
            "id": "1uNFoZAHBGtllmzznpCI3s"
        },
        "Alan Walker": {
            "emoji": "👨‍🎤",
            "id": "7vk5e3vY1uw9plTHJAMwjN"
        },
        "The Weeknd": {
            "emoji": "👨‍🎤",
            "id": "1Xyo4u8uXC1ZmMpatF05PJ"
        }
    }
    
    featured_artists = list(artist_info.keys())
    artist_cols = st.columns(len(featured_artists))
    
    for i, artist in enumerate(featured_artists):
        with artist_cols[i]:
            # Display artist emoji (much more reliable than external images)
            st.write(f"{artist_info[artist]['emoji']}")
            st.markdown(f"**{artist}**")
            
            # Add Spotify link
            spotify_url = f"https://open.spotify.com/artist/{artist_info[artist]['id']}"
            st.markdown(f"[Spotify Profile]({spotify_url})")
                

# Add some information about how the recommendations work
with st.expander("How do the recommendations work?"):
    st.markdown("""
    ### How our music recommendation works:
    
    1. **Mood Selection**: 
       - You select your current mood from our predefined list of options.
    
    2. **Music Matching**:
       - We match your mood to relevant music genres, artists, and tracks.
       - We then use these as "seeds" to get personalized recommendations using the Spotify API.
    
    3. **Recommendation Display**:
       - We display a selection of tracks that best match your current emotional state.
       - Each recommendation includes the song title, artist, album art, and a link to listen on Spotify.
       - When available, we also provide an audio preview you can play directly in the app.
    
    The goal is to provide music that resonates with how you're feeling right now!
    """)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit and [Spotify API](https://open.spotify.com)")
