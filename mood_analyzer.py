import os
import google.generativeai as genai
from typing import Optional

# Set up Gemini API
def setup_gemini():
    """Set up and configure the Gemini API."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set. Please set it with your Gemini API key.")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def analyze_mood(journal_text: str) -> str:
    """
    Analyze the mood from the journal entry using Gemini API.
    
    Args:
        journal_text: A string containing the user's journal entry.
        
    Returns:
        A string representing the detected mood.
    """
    # Set up the prompt for Gemini
    prompt = f"""
    Based on the following journal entry, what is the primary mood or emotion of the writer?
    Choose the single most dominant mood from this list: Happy, Energetic, Relaxed, Calm, Sad, Anxious, Focused, Romantic, Nostalgic, Excited, Sleepy, Angry.
    
    Journal entry:
    {journal_text}
    
    Provide only the mood name and nothing else. Just one word from the list above.
    """
    
    try:
        # Initialize the Gemini model
        model = setup_gemini()
        
        # Generate the response
        response = model.generate_content(prompt)
        
        # Extract and clean the mood
        detected_mood = response.text.strip()
        
        # Validate the mood against our list
        valid_moods = ["Happy", "Energetic", "Relaxed", "Calm", "Sad", "Anxious", 
                      "Focused", "Romantic", "Nostalgic", "Excited", "Sleepy", "Angry"]
        
        # Normalize the mood (capitalize first letter)
        for mood in valid_moods:
            if detected_mood.lower() == mood.lower():
                return mood
        
        # If the detected mood is not in our list, default to "Relaxed"
        return "Relaxed"
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error in mood analysis: {str(e)}")
        
        # Return a default mood in case of error
        return "Relaxed"
