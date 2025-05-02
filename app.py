import streamlit as st
import os
from music_recommender import get_music_recommendations

# Set page configuration
st.set_page_config(
    page_title="Mood-Based Music Recommender",
    page_icon="🎵",
    layout="wide",
)

# App title and description
st.title("🎵 Mood-Based Music Recommender")
st.markdown("""
This app recommends music based on your current mood. Simply select your mood from the dropdown menu to get personalized music recommendations!
""")

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
    st.header("Your Music Recommendations")
    
    # Display detected mood with an emoji
    mood_emojis = {
        "Happy": "😊", "Energetic": "⚡", "Relaxed": "😌", "Calm": "🧘",
        "Sad": "😢", "Anxious": "😰", "Focused": "🧠", "Romantic": "❤️",
        "Nostalgic": "🕰️", "Excited": "🤩", "Sleepy": "😴", "Angry": "😠"
    }
    
    mood = st.session_state.detected_mood
    emoji = mood_emojis.get(mood, "🎵")
    
    st.subheader(f"Detected Mood: {emoji} {mood}")
    
    # Display recommendations
    if st.session_state.recommendations:
        if len(st.session_state.recommendations) > 0:
            st.markdown("### Songs that match your mood:")
            
            # Create a grid layout for recommendations
            cols = st.columns(3)
            
            for i, track in enumerate(st.session_state.recommendations):
                with cols[i % 3]:
                    st.markdown(f"""
                    **{track['name']}**  
                    Artist: {track['artist']}  
                    """)
                    
                    # Display the album art if available
                    if 'image_url' in track and track['image_url']:
                        st.markdown(f"<a href='{track['url']}' target='_blank'><img src='{track['image_url']}' width='150'></a>", unsafe_allow_html=True)
                    
                    # Add a link to listen to the track
                    if 'url' in track:
                        st.markdown(f"[Listen on Spotify]({track['url']})")
                        
                    # Add a preview player if available
                    if 'preview_url' in track and track['preview_url']:
                        st.audio(track['preview_url'], format='audio/mp3')
                    
                    st.markdown("---")
        else:
            st.info("No recommendations found for this mood. Try a different mood or journal entry.")
    else:
        st.info("Recommendations will appear here once your mood is analyzed.")

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
st.markdown("Created with ❤️ using Streamlit and Spotify API")
