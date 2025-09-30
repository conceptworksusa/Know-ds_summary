import streamlit as st
import streamlit.components.v1 as components
import time

# Custom class for processing queries
class QueryProcessor:
    def __init__(self):
        self.query_history = []
    
    def process_query(self, query):
        """Process the query and return a response"""
        # Add query to history
        self.query_history.append({
            'query': query,
            'timestamp': time.time(),
            'response': f"Processed: {query}"
        })
        
        # Simple processing logic - replace with your actual processing
        response = f"AI Response: I received your query '{query}'. This is a placeholder response."
        
        return response

# Initialize the query processor
if 'query_processor' not in st.session_state:
    st.session_state.query_processor = QueryProcessor()

# Clean UI - Just query input and mic button
st.title("Voice Assistant")

# Browser compatibility check
st.markdown("**Browser Check:**")
if st.button("Check Browser Support", key="browser_check"):
    browser_check_html = """
    <div id="browserInfo" style="padding: 10px; background: #f0f0f0; border-radius: 5px; margin: 10px 0;"></div>
    <script>
    var info = 'Browser: ' + navigator.userAgent + '<br>';
    info += 'Speech Recognition Support: ';
    if ('webkitSpeechRecognition' in window) {
        info += '✅ WebKit Speech Recognition supported';
    } else if ('SpeechRecognition' in window) {
        info += '✅ Standard Speech Recognition supported';
    } else {
        info += '❌ No speech recognition support';
    }
    info += '<br>Microphone Permission: ';
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        info += '✅ MediaDevices API available';
    } else {
        info += '❌ MediaDevices API not available';
    }
    document.getElementById('browserInfo').innerHTML = info;
    </script>
    """
    components.html(browser_check_html, height=100)

# Create two columns: query input and mic button
col1, col2 = st.columns([4, 1])

with col1:
    text_query = st.text_input("Enter your query:", placeholder="Type or speak your question...", key="query_input")

with col2:
    if st.button("🎤", key="mic_btn", help="Click to start voice input"):
        st.session_state.voice_triggered = True

# Process text query automatically
if text_query and text_query.strip():
    st.session_state.text_query = text_query.strip()
    st.session_state.voice_triggered = False

# Voice input with automatic STT and TTS
if hasattr(st.session_state, 'voice_triggered') and st.session_state.voice_triggered:
    st.session_state.voice_triggered = False
    
    # Automatic voice input - starts immediately
    voice_html = """
    <div style="text-align: center; padding: 20px;">
        <div id="status" style="margin: 10px; font-size: 16px; color: #007bff;">🎤 Listening... Speak now!</div>
    </div>
    
    <script>
    // Auto-start voice recognition immediately
    function startVoiceRecognition() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            document.getElementById('status').innerHTML = 'Speech recognition not supported in this browser.';
            return;
        }
        
        var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        var recognition = new SpeechRecognition();
        
        recognition.lang = 'en-US';
        recognition.continuous = false;
        recognition.interimResults = false;
        
        recognition.onstart = function() {
            document.getElementById('status').innerHTML = '🎤 Listening... Speak clearly!';
        };
        
        recognition.onresult = function(event) {
            var transcript = event.results[0][0].transcript;
            document.getElementById('status').innerHTML = '✅ Processing: "' + transcript + '"';
            
            // Submit immediately
            setTimeout(function() {
                submitVoice(transcript);
            }, 500);
        };
        
        recognition.onerror = function(event) {
            document.getElementById('status').innerHTML = 'Error: ' + event.error;
        };
        
        recognition.onend = function() {
            document.getElementById('status').innerHTML = 'Voice recognition ended.';
        };
        
        // Start immediately
        recognition.start();
    }
    
    function submitVoice(transcript) {
        var form = document.createElement('form');
        form.method = 'POST';
        form.action = window.location.href;
        
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'voice_transcript';
        input.value = transcript;
        
        form.appendChild(input);
        document.body.appendChild(form);
        form.submit();
    }
    
    // Start voice recognition immediately when page loads
    document.addEventListener('DOMContentLoaded', function() {
        startVoiceRecognition();
    });
    </script>
    """
    
    components.html(voice_html, height=100)

# Handle text query with TTS
if hasattr(st.session_state, 'text_query'):
    query = st.session_state.text_query
    del st.session_state.text_query
    
    # Process the query
    response = st.session_state.query_processor.process_query(query)
    
    # Display response
    st.write(f"**Response:** {response}")
    
    # TTS for text response
    tts_html = f"""
    <script>
    if ('speechSynthesis' in window) {{
        var utterance = new SpeechSynthesisUtterance('{response.replace("'", "\\'")}');
        utterance.rate = 0.9;
        utterance.pitch = 1;
        utterance.volume = 0.8;
        speechSynthesis.speak(utterance);
    }}
    </script>
    """
    components.html(tts_html, height=0)

# Handle voice transcript with TTS
if 'voice_transcript' in st.query_params:
    query = st.query_params['voice_transcript']
    
    # Process the query
    response = st.session_state.query_processor.process_query(query)
    
    # Display response
    st.write(f"**Voice Query:** {query}")
    st.write(f"**Response:** {response}")
    
    # TTS for voice response
    tts_html = f"""
    <script>
    if ('speechSynthesis' in window) {{
        var utterance = new SpeechSynthesisUtterance('{response.replace("'", "\\'")}');
        utterance.rate = 0.9;
        utterance.pitch = 1;
        utterance.volume = 0.8;
        speechSynthesis.speak(utterance);
    }}
    </script>
    """
    components.html(tts_html, height=0)
