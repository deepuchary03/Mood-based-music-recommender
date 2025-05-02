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
                    # Card container with shadow and hover effect
                    st.markdown(f"""
                    <div style="
                        background-color: white; 
                        border-radius: 10px; 
                        padding: 15px; 
                        margin-bottom: 20px; 
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                        transition: transform 0.3s;
                        height: 380px;
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                    ">
                        <div>
                            <h3 style="margin-top: 0; font-size: 16px; color: #191414; font-weight: bold; overflow-wrap: break-word;">{track['name']}</h3>
                            <p style="color: #666; font-size: 14px; margin-top: 5px; font-style: italic;">{track['artist']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display the album art if available
                    if 'image_url' in track and track['image_url']:
                        st.markdown(f"""
                        <div style="text-align: center; margin: 10px 0;">
                            <a href="{track['url']}" target="_blank">
                                <img src="{track['image_url']}" style="width: 180px; height: 180px; object-fit: cover; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Add a preview player if available
                    if 'preview_url' in track and track['preview_url']:
                        st.audio(track['preview_url'], format='audio/mp3')
                    
                    # Add a link to listen to the track
                    if 'url' in track:
                        st.markdown(f"""
                        <div style="text-align: center; margin-top: 10px;">
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
                        """, unsafe_allow_html=True)
        else:
            st.info("No recommendations found for this mood. Try a different mood.")
    else:
        st.info("Recommendations will appear here once your mood is analyzed.")
        
    # Add an artist feature section
    st.markdown("<hr style='margin: 30px 0; height: 2px; background: linear-gradient(to right, #1DB954, #191414);'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>Your Favorite Artists</h3>", unsafe_allow_html=True)
    
    # Artist images and Spotify IDs (using more reliable image URLs)
    artist_info = {
        "Taylor Swift": {
            "image": "https://www.billboard.com/wp-content/uploads/2022/11/taylor-swift-2022-billboard-espanol-power-list-billboard-espanol-1548.jpg",
            "id": "06HL4z0CvFAxyc27GXpf02"
        },
        "Selena Gomez": {
            "image": "https://media1.popsugar-assets.com/files/thumbor/hnVKqXE-xPM5bi3w8RQLqFCDw_E/475x60:1974x1559/fit-in/2048xorig/filters:format_auto-!!-:strip_icc-!!-/2019/09/09/023/n/1922398/9f849ffa5d76e13d154137.01128738_/i/Selena-Gomez.jpg",
            "id": "0C8ZW7ezQVs4URX5aX7Kqx"
        },
        "Ed Sheeran": {
            "image": "https://www.rollingstone.com/wp-content/uploads/2021/08/ed-sheeran-new-album.jpg",
            "id": "6eUKZXaKkcviH0Ku9w2n3V"
        },
        "Justin Bieber": {
            "image": "https://www.rollingstone.com/wp-content/uploads/2021/03/Justin-Bieber-1.jpg",
            "id": "1uNFoZAHBGtllmzznpCI3s"
        },
        "Alan Walker": {
            "image": "https://edm.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cq_auto:good%2Cw_1200/MTU5NDY5ODMxOTk0MzcyODMx/alan-walker-supplied-press-photo.jpg",
            "id": "7vk5e3vY1uw9plTHJAMwjN"
        },
        "The Weeknd": {
            "image": "https://www.rollingstone.com/wp-content/uploads/2020/09/TheWeeknd.jpg",
            "id": "1Xyo4u8uXC1ZmMpatF05PJ"
        }
    }
    
    featured_artists = list(artist_info.keys())
    artist_cols = st.columns(len(featured_artists))
    
    for i, artist in enumerate(featured_artists):
        with artist_cols[i]:
            # Artist card with circular image
            st.markdown(f"""
            <div style="text-align: center;">
                <a href="https://open.spotify.com/artist/{artist_info[artist]['id']}" target="_blank">
                    <img src="{artist_info[artist]['image']}" style="
                        width: 80px; 
                        height: 80px; 
                        border-radius: 50%; 
                        object-fit: cover;
                        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
                        margin-bottom: 10px;
                    ">
                </a>
                <p style="font-weight: bold; margin: 5px 0 0 0; font-size: 14px;">{artist}</p>
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
