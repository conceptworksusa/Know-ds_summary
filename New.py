import streamlit as st
import speech_recognition as sr
import pyttsx3
import sys
import threading
import time

# Configure page
st.set_page_config(
    page_title="Voice Chat Assistant",
    page_icon="🎤",
    layout="wide"
)

# Initialize speech recognition and text-to-speech
@st.cache_resource
def get_speech_recognizer():
    return sr.Recognizer()

def speak_text(text):
    """Convert text to speech"""
    try:
        # Use subprocess to call system TTS (works better with Streamlit)
        import subprocess
        import platform
        
        if platform.system() == "Windows":
            # Use Windows SAPI
            subprocess.run(['powershell', '-Command', f'Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{text}")'], 
                          capture_output=True, timeout=10)
        else:
            # Use espeak for Linux/Mac
            subprocess.run(['espeak', text], capture_output=True, timeout=10)
            
    except Exception as e:
        # Fallback to pyttsx3 if system TTS fails
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except:
            pass

# Initialize components
recognizer = get_speech_recognizer()

def listen_to_voice():
    """Listen to microphone and return transcribed text"""
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            return text
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except Exception as e:
        return None

def chat(query):
    return f"This is your query: {query}"

# Initialize session state
msg_key = "chat_messages"
op_key = "chat_operation"

# Sidebar
st.sidebar.title("🎤 Voice Chat Assistant")
st.sidebar.markdown("How can I help you!")

if st.sidebar.button("🔄 Refresh"):
    st.session_state[msg_key] = []
    st.session_state[op_key] = None

# Initialize session state variables
if msg_key not in st.session_state:
    st.session_state[msg_key] = []
if op_key not in st.session_state:
    st.session_state[op_key] = None

# Main chat interface
st.title("🎤 Voice Chat Assistant")

# Display chat messages from history
for message in st.session_state[msg_key]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Custom chat input with mic button
col1, col2 = st.columns([6, 1])

with col1:
    query = st.chat_input("Ask anything...")

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    mic_button = st.button("🎤", help="Click to speak", key="mic_button", use_container_width=True)

# Process voice input
if mic_button:
    with st.spinner("🎤 Listening..."):
        voice_text = listen_to_voice()
        if voice_text:
            st.success(f"✅ Heard: {voice_text}")
            # Store voice text for processing
            st.session_state.voice_query = voice_text
        else:
            st.error("❌ Could not understand speech")

# Get query from either text input or voice input
current_query = query if query else st.session_state.get('voice_query', '')

# Process query
if current_query and current_query.strip():
    # Add user message to chat history
    st.session_state[msg_key].append({"role": "user", "content": current_query})

    # Display user message
    with st.chat_message("user"):
        st.markdown(f"***Question:*** {current_query}")

    # Process Q&A query
    try:
        response_placeholder = st.empty()
        response_placeholder.info("Loading...")
        response = chat(current_query)
    except Exception as e:
        response = f"There was an error while processing your request: {e}"
    finally:
        # Clear voice query after processing
        if 'voice_query' in st.session_state:
            del st.session_state.voice_query

    # Display assistant's response
    with st.chat_message("assistant"):
        # Clear the response placeholder
        response_placeholder.empty()
        st.markdown(f"***Answer:*** {response}")

    # Add assistant response to chat history
    st.session_state[msg_key].append({"role": "assistant", "content": response})

    # Automatically speak the response
    with st.spinner("🔊 Speaking response..."):
        speak_text(response)

# Custom CSS for buttons
st.markdown(
    """
    <style>
        .stButton>button { 
            width: 200px;   /* Set button width */
            height: 45px;   /* Set button height */
            font-size: 14px; /* Set button font size */
        }
        .stChatInput {
            width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True,
      )
