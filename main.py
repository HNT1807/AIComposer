import streamlit as st
import os
from bark import SAMPLE_RATE, generate_audio, preload_models
import numpy as np

# Set page configuration
st.set_page_config(layout="centered", page_title="AI Composer")

# Custom CSS to center everything and style the title
st.markdown("""
<style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
    }
    .big-title {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton > button {
        display: block;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='big-title'>AI COMPOSER</h1>", unsafe_allow_html=True)

# Model selection dropdown
model_option = st.selectbox(
    "Select Model",
    ("Regular", "Small"),
    index=0  # Default to Regular
)

# Set environment variable based on model selection
if model_option == "Small":
    os.environ["SUNO_USE_SMALL_MODELS"] = "True"
else:
    os.environ["SUNO_USE_SMALL_MODELS"] = "False"

# Text input
user_input = st.text_area("Enter your text prompt:", height=150)

# Generate button
if st.button("GENERATE"):
    if user_input:
        with st.spinner("Generating audio..."):
            # Ensure models are loaded
            preload_models()

            # Generate audio
            audio_array = generate_audio(user_input)

            # Convert to 32-bit float
            audio_array = audio_array.astype(np.float32)

            # Display audio player
            st.audio(audio_array, sample_rate=SAMPLE_RATE)
    else:
        st.warning("Please enter a text prompt.")

# Instructions
st.markdown("""
### Instructions:
1. Select the model you want to use (Regular or Small).
2. Enter your text prompt in the box above.
3. Start and end with ♪ for songs, for example "♪ In the jungle, the mighty jungle, the lion barks tonight ♪"
4. You can include special instructions like `[laughter]`, `[laughs]`, `[gasps]`, `[clears throat]`, `[sighs]`, `[MAN]` and `[WOMAN]`, `—` or `...` for hesitations, or CAPITALIZATION for emphasis of a word, for example " [MAN] Hello, my name is Suno. And, uh — and I like... PIZZA. [laughs]"
5. You can use foreign languages.
6. Click the 'GENERATE' button to create audio.
7. Wait for the audio to generate (this may take a moment).
8. Play the generated audio using the audio player that appears.

Note: The Small model is faster but may produce lower quality audio.
""")