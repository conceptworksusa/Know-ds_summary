# Import necessary libraries
import streamlit as st
import sys

sys.path.append(r'C:\PycharmProjects\Knowtion-ds_summary')
from src.api.TextSummarizer import TextSummarizer
from src.conf.Prompts import system_prompt
from src.ui import header

page_id = "chat"
msg_key = f"{page_id}_messages"
op_key = f"{page_id}_operation"


# Welcome message
header.show_sidebar_logo("This is a Custom Summarization Assistant!!")

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
    contain = st.container(height=137, border=True)
    contain.title("**Document Selection**")
    # st.session_state.doc_id = contain.text_area("Enter the document ID", value="")
    col1, col2 = contain.columns([2,2])
    with col1:
        st.markdown("### Document ID :")
    with col2:
        st.session_state.doc_id = st.text_input("", value="", placeholder="Enter the document ID", label_visibility="collapsed")

    contain = st.container(height=165, border=True)
    contain.title("**LLM model**")
    st.session_state.model = contain.selectbox("Select the model", ["llama3.1" , "Mistral"])

    if st.button("🔄 Refresh"):
        st.session_state.msg_key = []
        st.session_state.op_key = None

# Display chat messages from history
for message in st.session_state.msg_key:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process Summarization with custom prompt
if custom_prompt := st.chat_input(system_prompt):
    # Add user message to chat history
    st.session_state.msg_key.append({"role": "user", "content": custom_prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(f"***Your Prompt:*** {custom_prompt}")

    try:
        if st.session_state.doc_id:
            response = TextSummarizer().summarize(doc_id=st.session_state.doc_id,prompt=custom_prompt, llama_model=st.session_state.model)

            # Display assistant's response
            with st.chat_message("assistant"):
                st.markdown(f"***Summary:*** {response}")

            # Add assistant response to chat history
            st.session_state.msg_key.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error(f"There was an error while processing the summarization: {e}")

    finally:
        # Clear input field
        st.session_state.doc_id = None

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
