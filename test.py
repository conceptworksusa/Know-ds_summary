import streamlit as st

# Custom class (you can replace with your logic)
class ElevatorAssistant:
    def answer(self, query: str) -> str:
        return f"You said: {query} (handled by ElevatorAssistant)"

assistant = ElevatorAssistant()

st.set_page_config(page_title="Voice + Text Assistant", page_icon="🎤", layout="centered")

st.title("🎤 Elevator Assistant (Voice + Text)")

# --- Input Section ---
st.write("You can either type or use the mic to speak")

# Text Input
user_text = st.text_input("Type your query here:")

# Voice Input via Web Speech API
st.markdown(
    """
    <button onclick="startRecognition()">🎙 Speak</button>
    <p id="speechResult"></p>

    <script>
    var recognition;
    function startRecognition() {
        if (!('webkitSpeechRecognition' in window)) {
            alert("Your browser does not support Speech Recognition (try Chrome).");
            return;
        }
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-US";

        recognition.onresult = function(event) {
            var result = event.results[0][0].transcript;
            document.getElementById('speechResult').innerText = result;
            var streamlitInput = document.querySelector('input[type="text"]');
            if(streamlitInput){
                streamlitInput.value = result;
                streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
        };

        recognition.start();
    }
    </script>
    """,
    unsafe_allow_html=True
)

# --- Process Query ---
query = user_text.strip() if user_text else None
if query:
    response = assistant.answer(query)
    st.success(response)

    # Trigger TTS
    st.markdown(
        f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{response}");
        window.speechSynthesis.speak(msg);
        </script>
        """,
        unsafe_allow_html=True
    )
