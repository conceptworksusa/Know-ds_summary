# Import necessary libraries
import streamlit as st
import sys

sys.path.append(r'C:\Users\skarnatapu\source\repos\Knowtion-ds_summary\KnowtionServices')
from src.api.OllamaParser import OllamaParser

from src.ui import header

page_id = "chat"
msg_key = f"{page_id}_messages"
op_key = f"{page_id}_operation"


# Welcome message
header.show_sidebar_logo("This is a billing story assistant!!")

# Initialize session state variables
if msg_key not in st.session_state:
    st.session_state.msg_key = []
if op_key not in st.session_state:
    st.session_state.op_key = None
if "doc_id" not in st.session_state:
    st.session_state.doc_id = None

def clear_input():
    """Clear the input field."""
    st.session_state.doc_id = None
    st.session_state.op_key = None

# Sidebar for selecting document and operation
with st.sidebar:

    contain = st.container(height=165, border=True)
    contain.title("**LLM model**")
    st.session_state.model = contain.selectbox("Select the model", ["llama3.1" , "Mistral"])

    contain = st.container(height=165, border=True)
    st.session_state.file = contain.selectbox("Select document", [None, "BillingStory.json",
                                                                   "BillingStory_AmpShardUnityPoint_217608_20250424_133941.json",
                                                                   "BillingStory_AmpShardUnityPoint_323541_20250424_133942.json",
                                                                   "BillingStory_AmpShardUnityPoint_330547_20250424_133945.json"])
    st.session_state.op_key = contain.button("Get Story")


    if st.button("🔄 Refresh"):
        st.session_state.msg_key = []
        st.session_state.op_key = None

# Display chat messages from history
for message in st.session_state.msg_key:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.op_key:
    file_name = st.session_state.file

    # Display file
    with st.chat_message("user"):
        st.markdown(f"***Your File:*** {file_name}")

    # Add user message to chat history
    st.session_state.msg_key.append({"role": "user", "content": file_name})


    response = OllamaParser().get_story(file_name)

    # Display assistant's response
    with st.chat_message("assistant"):
        st.markdown(f"***Story:*** {response}")

    # Add assistant response to chat history
    st.session_state.msg_key.append({"role": "assistant", "content": response})

clear_input()


# Custom CSS for buttons
st.markdown(
    """
    <style>
        .stButton>button { 
            width: 200px;   /* Set button width */
            height: 45px;   /* Set button height */
            font-size: 14px; /* Set button font size */
        }
    </style>
    """,
    unsafe_allow_html=True,
)
