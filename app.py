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

# App title and description with emoji
st.markdown("<h1>🎵 Mood-Based Music Recommender</h1>", unsafe_allow_html=True)
st.markdown("<p class='description'>Get personalized music recommendations based on your current mood featuring your favorite artists!</p>", unsafe_allow_html=True)

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
    
    st.markdown(f"<h2 style='text-align: center; color: #1DB954;'>Your {mood} {emoji} Music</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Featuring songs from your favorite artists</p>", unsafe_allow_html=True)
    
    # Display recommendations
    if st.session_state.recommendations:
        if len(st.session_state.recommendations) > 0:
            # Create a grid layout for recommendations
            cols = st.columns(3)
            
            for i, track in enumerate(st.session_state.recommendations):
                with cols[i % 3]:
                    # New design with album art as background and song info at the bottom
                    image_url = track.get('image_url', '')
                    
                    # Create the card container
                    st.markdown(f"""
                    <div style="
                        background-color: white; 
                        border-radius: 10px; 
                        margin-bottom: 20px; 
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                        overflow: hidden;
                        height: 300px;
                        position: relative;
                    ">
                        <a href="{track['url']}" target="_blank" style="text-decoration: none; color: inherit;">
                            <div style="
                                width: 100%;
                                height: 100%;
                                background-image: url('{image_url}');
                                background-size: cover;
                                background-position: center;
                                position: relative;
                            ">
                                <div style="
                                    position: absolute;
                                    top: 0;
                                    left: 0;
                                    right: 0;
                                    padding: 10px 15px;
                                    background-color: rgba(0,0,0,0.7);
                                    color: white;
                                    font-weight: bold;
                                    font-size: 16px;
                                    text-align: center;
                                    white-space: nowrap;
                                    overflow: hidden;
                                    text-overflow: ellipsis;
                                ">
                                    {track['name']}
                                </div>
                                <div style="
                                    position: absolute;
                                    bottom: 0;
                                    left: 0;
                                    right: 0;
                                    padding: 15px;
                                    background-color: rgba(255,255,255,0.9);
                                ">
                                    <p style="margin: 0; font-size: 14px; color: #333;">{track['artist']}</p>
                                    <div style="margin-top: 10px; text-align: center;">
                                        <a href="{track['url']}" target="_blank" style="
                                            display: inline-block;
                                            text-decoration: none;
                                            color: white;
                                            background-color: #1DB954;
                                            padding: 8px 15px;
                                            border-radius: 20px;
                                            font-size: 14px;
                                            font-weight: bold;
                                            transition: background-color 0.3s;
                                        ">Listen on Spotify</a>
                                    </div>
                                </div>
                            </div>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add a preview player if available (outside the card for better usability)
                    if 'preview_url' in track and track['preview_url']:
                        st.audio(track['preview_url'], format='audio/mp3')
        else:
            st.info("No recommendations found for this mood. Try a different mood.")
    else:
        st.info("Recommendations will appear here once your mood is analyzed.")
        
    # Add an artist feature section
    st.markdown("<hr style='margin: 30px 0; height: 2px; background: linear-gradient(to right, #1DB954, #191414);'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>Your Favorite Artists</h3>", unsafe_allow_html=True)
    
    # Simple SVG colors for each artist as fallback - guaranteed to work
    artist_info = {
        "Taylor Swift": {
            "image": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='50' fill='%23dc143c'/%3E%3Ctext x='50%25' y='50%25' font-size='20' text-anchor='middle' dominant-baseline='middle' fill='white'%3ETS%3C/text%3E%3C/svg%3E",
            "id": "06HL4z0CvFAxyc27GXpf02",
            "color": "#dc143c"
        },
        "Selena Gomez": {
            "image": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='50' fill='%23ff69b4'/%3E%3Ctext x='50%25' y='50%25' font-size='20' text-anchor='middle' dominant-baseline='middle' fill='white'%3ESG%3C/text%3E%3C/svg%3E",
            "id": "0C8ZW7ezQVs4URX5aX7Kqx",
            "color": "#ff69b4"
        },
        "Ed Sheeran": {
            "image": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='50' fill='%23ff7f50'/%3E%3Ctext x='50%25' y='50%25' font-size='20' text-anchor='middle' dominant-baseline='middle' fill='white'%3EES%3C/text%3E%3C/svg%3E",
            "id": "6eUKZXaKkcviH0Ku9w2n3V",
            "color": "#ff7f50"
        },
        "Justin Bieber": {
            "image": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='50' fill='%234169e1'/%3E%3Ctext x='50%25' y='50%25' font-size='20' text-anchor='middle' dominant-baseline='middle' fill='white'%3EJB%3C/text%3E%3C/svg%3E",
            "id": "1uNFoZAHBGtllmzznpCI3s",
            "color": "#4169e1"
        },
        "Alan Walker": {
            "image": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='50' fill='%23696969'/%3E%3Ctext x='50%25' y='50%25' font-size='20' text-anchor='middle' dominant-baseline='middle' fill='white'%3EAW%3C/text%3E%3C/svg%3E",
            "id": "7vk5e3vY1uw9plTHJAMwjN",
            "color": "#696969"
        },
        "The Weeknd": {
            "image": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='50' fill='%23800080'/%3E%3Ctext x='50%25' y='50%25' font-size='20' text-anchor='middle' dominant-baseline='middle' fill='white'%3ETW%3C/text%3E%3C/svg%3E",
            "id": "1Xyo4u8uXC1ZmMpatF05PJ",
            "color": "#800080"
        }
    }
    
    featured_artists = list(artist_info.keys())
    artist_cols = st.columns(len(featured_artists))
    
    for i, artist in enumerate(featured_artists):
        with artist_cols[i]:
            # Artist card with circular image and gradient border
            color = artist_info[artist]['color']
            st.markdown(f"""
            <div style="text-align: center;">
                <a href="https://open.spotify.com/artist/{artist_info[artist]['id']}" target="_blank">
                    <div style="
                        width: 90px;
                        height: 90px;
                        border-radius: 50%;
                        padding: 4px;
                        background: linear-gradient(45deg, {color}, #1DB954);
                        margin: 0 auto;
                        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                        transition: transform 0.3s;
                    ">
                        <img src="{artist_info[artist]['image']}" style="
                            width: 100%;
                            height: 100%;
                            border-radius: 50%;
                            object-fit: cover;
                            border: 2px solid white;
                        ">
                    </div>
                </a>
                <p style="font-weight: bold; margin: 10px 0 0 0; font-size: 15px; color: #333;">{artist}</p>
            </div>
            """, unsafe_allow_html=True)

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
st.markdown("<hr style='margin-top: 40px; margin-bottom: 20px; height: 2px; background: linear-gradient(to right, #1DB954, #191414);'>", unsafe_allow_html=True)
st.markdown("<p class='footer'>Created with ❤️ using Streamlit and <a href='https://open.spotify.com' target='_blank' style='color: #1DB954; text-decoration: none;'>Spotify API</a></p>", unsafe_allow_html=True)
