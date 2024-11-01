import streamlit as st
import speech_recognition as sr
import time
import os
from progressbar import ProgressBar, Percentage, Bar

# Initialize recognizer class and adjust for noise
r = sr.Recognizer()


# Function to transcribe speech
def transcribe_speech(api_choice, language="en-US"):
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        st.info("Speak now...")
        
        audio_text = r.listen(source)

        st.info("Transcribing now...")        
        # Show progress bar when transcribing
        with st.spinner("Transcribing..."):
            time.sleep(3)  

            try:
                # API options
                if api_choice == "Google":
                    text = r.recognize_google(audio_text, language=language).lower()
                elif api_choice == "Sphinx":
                    text = r.recognize_sphinx(audio_text).lower()
                else:
                    st.error("Selected API is not supported., choose the available ones")
                    return None

                st.success("YAAY! Transcription complete!")
                st.write("Did you say: ", text)
                return text
            except sr.RequestError as e:
                st.error(f"API request failed; {e}")
                return None
            except sr.UnknownValueError:
                st.error("Sorry, I could not understand the audio.")
                return None


# Function to save text to a file
def save_transcription(text):
    if text:
        file_path = "transcription.txt"  # Specify the path explicitly
        with open(file_path, "a") as f:
            f.write(text + "\n")
        st.success(f"Transcription saved to {file_path}")
        st.info(f"File path: {os.path.abspath(file_path)}")  # Show the absolute file path


def main():
    st.title("Speech Recognition App")
    st.write("Click the button below and speak and your speech will be transcribed.")

    # Select speech recognition API
    api_choice = st.selectbox("Choose an API", ("Google", "Sphinx"))
    
    # Select language for recognition
    language = st.selectbox("Choose a language", ("en-US", "en-GB")) 
    
    # Button to start recording
    if st.button("Start Recording"):
        text = transcribe_speech(api_choice, language)
        if text:
            # Option to save transcription
            if st.checkbox("Save Transcription to a text file"):
                save_transcription(text)

if __name__ == "__main__":
    main()
