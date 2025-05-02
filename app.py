import streamlit as st
import os
from mood_analyzer import analyze_mood
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
This app recommends music based on your current mood. You can either:
- Select your mood directly from the dropdown menu, or
- Enter a journal entry about how you're feeling, and we'll analyze it for you!
""")

# Initialize session state variables if they don't exist
if 'detected_mood' not in st.session_state:
    st.session_state.detected_mood = None
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'journal_text' not in st.session_state:
    st.session_state.journal_text = ""

# Create two columns for the two input methods
col1, col2 = st.columns(2)

# Column 1: Direct mood selection
with col1:
    st.header("Select Your Mood")
    
    moods = [
        "Happy", "Energetic", "Relaxed", "Calm", 
        "Sad", "Anxious", "Focused", "Romantic",
        "Nostalgic", "Excited", "Sleepy", "Angry"
    ]
    
    selected_mood = st.selectbox("Choose your current mood:", [""] + moods, index=0)
    
    if st.button("Get Recommendations from Selection"):
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

# Column 2: Journal entry analysis
with col2:
    st.header("Analyze Your Journal Entry")
    
    journal_text = st.text_area(
        "Write about how you're feeling today...",
        value=st.session_state.journal_text,
        height=150
    )
    
    if st.button("Analyze My Mood"):
        if journal_text.strip():
            st.session_state.journal_text = journal_text
            
            with st.spinner("Analyzing your mood..."):
                try:
                    detected_mood = analyze_mood(journal_text)
                    st.session_state.detected_mood = detected_mood
                    
                    # Get music recommendations based on the detected mood
                    with st.spinner(f"Finding music for your {detected_mood.lower()} mood..."):
                        st.session_state.recommendations = get_music_recommendations(detected_mood)
                        st.rerun()
                except Exception as e:
                    st.error(f"Error analyzing mood: {str(e)}")
        else:
            st.warning("Please enter some text about how you're feeling.")

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
                        st.markdown(f"[Listen on Deezer]({track['url']})")
                    
                    st.markdown("---")
        else:
            st.info("No recommendations found for this mood. Try a different mood or journal entry.")
    else:
        st.info("Recommendations will appear here once your mood is analyzed.")

# Add some information about how the recommendations work
with st.expander("How do the recommendations work?"):
    st.markdown("""
    ### How our music recommendation works:
    
    1. **Mood Detection**: 
       - When you select a mood directly, we use that selection.
       - When you provide a journal entry, we use Google's Gemini AI to analyze the sentiment and identify your mood.
    
    2. **Music Matching**:
       - We match your mood to relevant music genres and keywords.
       - We then search for top tracks that match these criteria using the Deezer API.
    
    3. **Recommendation Display**:
       - We display a selection of tracks that best match your current emotional state.
       - Each recommendation includes the song title, artist, and a link to listen to it.
    
    The goal is to provide music that resonates with how you're feeling right now!
    """)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit and Google's Gemini AI")
