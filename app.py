import streamlit as st
import os
from music_recommender import get_music_recommendations

# Set page configuration
st.set_page_config(
    page_title="Mood-Based Music Recommender",
    page_icon="🎵",
    layout="wide",
)

st.markdown("""
<style>
  
    [data-testid="stToolbar"] {
        background-color: transparent !important;
        height: 0 !important;
        visibility: hidden !important;
    }

    /* Ensure no padding or margin around the toolbar */
    [data-testid="stToolbar"]::before {
        content: '';
        display: none;
    }

 
    .main, .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebarContent"] {
        background-color: #121212 !important;
        color: white !important;
    }

    /* Remove any white space or padding at the top of the app */
    [data-testid="stDecoration"] {
        background-color: transparent !important;
    }
    [data-testid="stHeader"] {
        background-color: transparent !important;
        height: 0 !important;
        visibility: hidden !important;
    }
</style>
""", unsafe_allow_html=True)

# Custom CSS - Spotify themed dark mode
st.markdown("""
<style>
    /* Set a consistent dark background for the entire app */
    .main, .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebarContent"] {
        background-color: #121212 !important;
        color: white !important;
    }

    /* Set consistent text colors */
    h1, h2, h3, h4, h5, p, label, div.stMarkdown p {
        color: #DDDDDD !important;
    }

    /* Style buttons */
    .stButton>button {
        background-color: #1DB954 !important;
        color: white !important;
        border: none !important;
        padding: 0.5em 2em !important;
        border-radius: 30px !important;
    }
    .stButton>button:hover {
        background-color: #14943E !important;
    }

    /* Style selectbox and dropdowns */
    div[data-baseweb="select"] {
        background-color: #212121 !important; /* Dark background */
        border-color: #333 !important; /* Dark border */
    }
    div[data-baseweb="select"] > div {
        background-color: #212121 !important; /* Dark background */
    }
    div[data-baseweb="select"] div {
        color: white !important; /* White text */
    }
    div[data-baseweb="select"] span {
        color: white !important; /* White text */
    }
    div[data-baseweb="popover"] {
        background-color: #212121 !important; /* Dark background for dropdown */
    }
    div[role="listbox"] {
        background-color: #212121 !important; /* Dark background for options */
    }
    div[role="option"] {
        background-color: #212121 !important; /* Dark background for each option */
        color: white !important; /* White text for each option */
    }
    div[role="option"]:hover {
        background-color: #333333 !important; /* Slightly lighter background on hover */
    }

    /* Fix text visibility in dark mode */
    .css-10oheav, .css-1b0udgb, .css-1aumxhk, .st-emotion-cache-16txnqn, .st-emotion-cache-1xw8zd0, .st-emotion-cache-1offfbd p, .st-emotion-cache-10oheav, .st-emotion-cache-1qg75ux {
        color: white !important;
        background-color: #121212 !important;
    }

    /* Footer styling */
    .footer {
        text-align: center;
        margin-top: 2em;
        color: #555;
    }

    /* Horizontal rule styling */
    hr {
        margin: 25px 0;
        height: 3px;
        background: linear-gradient(to right, #1DB954, #191414);
        border: none;
    }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
    /* Hide the Streamlit menu bar and make it transparent */
    [data-testid="stToolbar"] {
        background-color: transparent !important;
        height: 0 !important;
        visibility: hidden !important;
    }

    /* Ensure no padding or margin around the toolbar */
    [data-testid="stToolbar"]::before {
        content: '';
        display: none;
    }

    /* Set a consistent dark background for the entire app */
    .main, .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebarContent"] {
        background-color: #121212 !important;
        color: white !important;
    }

    /* Remove any white space or padding at the top of the app */
    [data-testid="stDecoration"] {
        background-color: transparent !important;
    }
    [data-testid="stHeader"] {
        background-color: transparent !important;
        height: 0 !important;
        visibility: hidden !important;
    }
</style>
""", unsafe_allow_html=True)

# App title and description with emoji
st.markdown("<h1>🎵 Mood-Based Music Recommender</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='description'>Get personalized music recommendations based on your current mood featuring your favorite artists!</p>",
    unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if 'detected_mood' not in st.session_state:
    st.session_state.detected_mood = None
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None

# Mood selection
st.header("Select Your Mood")

moods = [
    "Happy", "Energetic", "Relaxed", "Calm", "Sad", "Anxious", "Focused",
    "Romantic", "Nostalgic", "Excited", "Sleepy", "Angry"
]

# Add direct inline styling for the selectbox
st.markdown("""
<style>
    /* Force selectbox to have light text on dark background */
    div[data-baseweb="select"] {background-color: #212121 !important; border-color: #333 !important;}
    div[data-baseweb="select"] > div {background-color: #212121 !important;}
    div[data-baseweb="select"] div {color: white !important;}
    div[data-baseweb="select"] span {color: white !important;}
    div[data-baseweb="popover"] {background-color: #212121 !important;}
    div[role="listbox"] {background-color: #212121 !important;}
    div[role="option"] {background-color: #212121 !important; color: white !important;}
    div[role="option"]:hover {background-color: #333333 !important;}
    
    /* Additional selectors to ensure text visibility */
    .st-emotion-cache-16txnqn {color: white !important;}
    .st-emotion-cache-1xw8zd0 {color: white !important; background-color: #212121 !important;}
    .st-emotion-cache-1offfbd p {color: white !important;}
    .st-emotion-cache-10oheav {color: white !important;}
    .st-emotion-cache-1qg75ux {color: white !important; background-color: #212121 !important;}
</style>
""",
            unsafe_allow_html=True)

selected_mood = st.selectbox("Choose your current mood:", [""] + moods,
                             index=0)

if st.button("Get Music Recommendations", type="primary"):
    if selected_mood:
        st.session_state.detected_mood = selected_mood
        with st.spinner(
                f"Finding music for your {selected_mood.lower()} mood..."):
            try:
                st.session_state.recommendations = get_music_recommendations(
                    selected_mood)
                st.rerun()
            except Exception as e:
                st.error(f"Error getting recommendations: {str(e)}")
    else:
        st.warning("Please select a mood first!")

# Display results section
if st.session_state.detected_mood:
    st.markdown(
        "<hr style='margin: 25px 0; height: 3px; background: linear-gradient(to right, #1DB954, #191414);'>",
        unsafe_allow_html=True)

    # Display detected mood with an emoji and styling
    mood_emojis = {
        "Happy": "😊",
        "Energetic": "⚡",
        "Relaxed": "😌",
        "Calm": "🧘",
        "Sad": "😢",
        "Anxious": "😰",
        "Focused": "🧠",
        "Romantic": "❤️",
        "Nostalgic": "🕰️",
        "Excited": "🤩",
        "Sleepy": "😴",
        "Angry": "😠"
    }

    mood = st.session_state.detected_mood
    emoji = mood_emojis.get(mood, "🎵")

    st.markdown(
        f"<h2 style='text-align: center; color: #1DB954;'>Your {mood} {emoji} Music</h2>",
        unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; margin-bottom: 30px;'>Featuring songs from your favorite artists</p>",
        unsafe_allow_html=True)

    # Display recommendations
    if st.session_state.recommendations:
        if len(st.session_state.recommendations) > 0:
            # Create a grid layout for recommendations - 3 columns
            cols = st.columns(3)
            st.write(
                f"Showing {len(st.session_state.recommendations)} recommendations for your {mood} mood"
            )

            for i, track in enumerate(st.session_state.recommendations):
                with cols[i % 3]:
                    # New design with album art as background and song info at the bottom
                    image_url = track.get('image_url', '')

                    # Check if we have a valid image URL from Spotify
                    if not image_url or image_url.strip() == "":
                        # Use a Spotify-themed placeholder if no image available
                        image_url = "https://developer.spotify.com/assets/branding-guidelines/icon3@2x.png"
                        st.warning(
                            f"Could not load album artwork for {track['name']}"
                        )

                    # Display album name to show we're using real data
                    album_name = track.get('album_name', '')

                    # Create a styled card with larger images and consistent dimensions
                    st.markdown(f"""
                    <div style="background-color: #121212; border-radius: 10px; padding: 0; margin-bottom: 20px; color: white; overflow: hidden;">
                        <div style="display: flex; flex-direction: column;">
                            <!-- Square album image with fixed dimensions -->
                            <div style="width: 100%; padding-bottom: 100%; position: relative; overflow: hidden;">
                                <img src="{image_url}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover;" alt="Album Cover">
                                <div style="position: absolute; top: 10px; right: 10px; background-color: rgba(0,0,0,0.7); border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center;">
                                    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/232px-Spotify_icon.svg.png" style="width: 20px; height: 20px;">
                                </div>
                            </div>
                            <!-- Track info in fixed height container - consistent 150px height -->
                            <div style="padding: 15px; height: 150px; display: flex; flex-direction: column; justify-content: space-between;">
                                <div>
                                    <h3 style="margin: 0 0 10px 0; font-size: 18px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{track['name']}</h3>
                                    <p style="margin: 0 0 5px 0; font-size: 14px;"><strong>Artist:</strong> {track['artist']}</p>
                                    <p style="margin: 0; font-size: 14px; color: #aaa;"><strong>Album:</strong> {album_name}</p>
                                </div>
                                <div>
                                    <a href="{track['url']}" target="_blank" style="
                                        display: inline-block;
                                        text-decoration: none;
                                        color: white;
                                        background-color: #1DB954;
                                        padding: 8px 15px;
                                        border-radius: 20px;
                                        font-size: 14px;
                                        font-weight: bold;
                                        width: 100%;
                                        text-align: center;
                                        box-sizing: border-box;">
                                        Listen on Spotify
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                    """,
                                unsafe_allow_html=True)

                    # Add a preview player if available (outside the card for better usability)
                    if 'preview_url' in track and track['preview_url']:
                        st.audio(track['preview_url'], format='audio/mp3')
        else:
            st.info(
                "No recommendations found for this mood. Try a different mood."
            )
    else:
        st.info("Recommendations will appear here once your mood is analyzed.")

    # Add an artist feature section
    st.markdown(
        "<hr style='margin: 30px 0; height: 2px; background: linear-gradient(to right, #1DB954, #191414);'>",
        unsafe_allow_html=True)
    st.markdown(
        "<h3 style='text-align: center; margin-bottom: 20px;'>Your Favorite Artists</h3>",
        unsafe_allow_html=True)

    # Artist images scraped directly from Spotify
    artist_info = {
        "Taylor Swift": {
            "image":
            "https://i.scdn.co/image/ab6761610000e5ebe672b5f553298dcdccb0e676",
            "id": "06HL4z0CvFAxyc27GXpf02"
        },
        "Selena Gomez": {
            "image":
            "https://i.scdn.co/image/ab6761610000e5eb815e520e3ce7fe210046ba66",
            "id": "0C8ZW7ezQVs4URX5aX7Kqx"
        },
        "Ed Sheeran": {
            "image":
            "https://i.scdn.co/image/ab6761610000e5eb399444ed4eace08b549d1161",
            "id": "6eUKZXaKkcviH0Ku9w2n3V"
        },
        "Justin Bieber": {
            "image":
            "https://i.scdn.co/image/ab6761610000e5eb8ae7f2aaa9817a704a87ea36",
            "id": "1uNFoZAHBGtllmzznpCI3s"
        },
        "Alan Walker": {
            "image":
            "https://i.scdn.co/image/ab6761610000e5ebbf753c009fd9c2d53351dd3c",
            "id": "7vk5e3vY1uw9plTHJAMwjN"
        },
        "The Weeknd": {
            "image":
            "https://i.scdn.co/image/ab6761610000e5eb9e528993a2820267b97f6aae",
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
                        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                        margin-bottom: 10px;
                    ">
                </a>
                <p style="font-weight: bold; margin: 5px 0 0 0; font-size: 14px;">{artist}</p>
            </div>
            """,
                        unsafe_allow_html=True)

# Add some information about how the recommendations work

# Footer
st.markdown(
    "<hr style='margin-top: 40px; margin-bottom: 20px; height: 2px; background: linear-gradient(to right, #1DB954, #191414);'>",
    unsafe_allow_html=True)

# Custom footer with profile image
st.markdown("""
<div style="text-align: center; margin-top: 2em;">
    © 2025 S Pranav
</div>
""",
            unsafe_allow_html=True)
