# Import necessary libraries
import streamlit as st
from src.api.OllamaParser import OllamaParser
from src.ui import header

page_id = "chat"
msg_key = f"{page_id}_messages"
op_key = f"{page_id}_operation"


# Welcome message
header.show_sidebar_logo("Billing story Assistant!!")

# Initialize session state variables
if msg_key not in st.session_state:
    st.session_state[msg_key] = []
if op_key not in st.session_state:
    st.session_state[op_key] = None


def clear_input():
    """Clear the input field."""
    st.session_state[op_key] = None

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
    st.session_state[op_key] = contain.button("Get Story")


    if st.button("🔄 Refresh"):
        st.session_state[msg_key] = []
        st.session_state[op_key] = None



if st.session_state[op_key]:
    file_name = st.session_state["file"]

    # Display file
    with st.chat_message("user"):
        st.markdown(f"***Your File:*** {file_name}")

    # Add user message to chat history
    st.session_state[msg_key].append({"role": "user", "content": file_name})


    response = OllamaParser().get_story(file_name)

    # Display assistant's response
    with st.chat_message("assistant"):
        st.markdown(f"***Story:*** {response}")

    # Add assistant response to chat history
    st.session_state[msg_key].append({"role": "assistant", "content": response})

clear_input()

# Display chat messages from history
for message in st.session_state[msg_key]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


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
# Import necessary libraries
import streamlit as st
from src.api.OllamaParser import OllamaParser
from src.ui import header

page_id = "chat"
msg_key = f"{page_id}_messages"
op_key = f"{page_id}_operation"


# Welcome message
header.show_sidebar_logo("Billing story Assistant!!")

# Initialize session state variables
if msg_key not in st.session_state:
    st.session_state[msg_key] = []
if op_key not in st.session_state:
    st.session_state[op_key] = None


def clear_input():
    """Clear the input field."""
    st.session_state[op_key] = None

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
    st.session_state[op_key] = contain.button("Get Story")


    if st.button("🔄 Refresh"):
        st.session_state[msg_key] = []
        st.session_state[op_key] = None



if st.session_state[op_key]:
    file_name = st.session_state["file"]

    # Display file
    with st.chat_message("user"):
        st.markdown(f"***Your File:*** {file_name}")

    # Add user message to chat history
    st.session_state[msg_key].append({"role": "user", "content": file_name})


    response = OllamaParser().get_story(file_name)

    # Display assistant's response
    with st.chat_message("assistant"):
        st.markdown(f"***Story:*** {response}")

    # Add assistant response to chat history
    st.session_state[msg_key].append({"role": "assistant", "content": response})

clear_input()

# Display chat messages from history
for message in st.session_state[msg_key]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


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




















# Import necessary libraries
import streamlit as st
from src.api.ChatBot import ChatBot
from src.ui import header

page_id = "qa"
msg_key = f"{page_id}_messages"
op_key = f"{page_id}_operation"

# Welcome message
header.show_sidebar_logo("This is a Q&A assistant!!")

# Initialize session state variables
if msg_key not in st.session_state:
    st.session_state[msg_key] = []
if op_key not in st.session_state:
    st.session_state[op_key] = None
if "doc_id" not in st.session_state:
    st.session_state.doc_id = None

def clear_input():
    """Clear the input field."""
    st.session_state.doc_id = None
    st.session_state[op_key] = None

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
        st.session_state[msg_key] = []
        st.session_state[op_key] = None

# Display chat messages from history
for message in st.session_state[msg_key]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input for Q&A
if prompt := st.chat_input("Enter your query..."):
    # Add user message to chat history
    st.session_state[msg_key].append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(f"***Question:*** {prompt}")

    # Process Q&A query
    try:
        response = ChatBot().get_response(prompt, st.session_state.doc_id)
    except Exception as e:
        response = f"There was an error while processing your request: {e}"

    finally:
        # Clear input field
        st.session_state.doc_id = None

    # Display assistant's response
    with st.chat_message("assistant"):
        st.markdown(f"***Answer:*** {response}")

    # Add assistant response to chat history
    st.session_state[msg_key].append({"role": "assistant", "content": response})

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



