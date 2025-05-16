# Import necessary libraries
import streamlit as st
import sys

import header

page_id = "chat"
msg_key = f"{page_id}_messages"
op_key = f"{page_id}_operation"

header.show_sidebar_logo("How can I help you!")

#sys.path.append(r'C:\Users\skarnatapu\source\repos\Knowtion-ds_summary\KnowtionServices')
sys.path.append(r'/code')


from src.api.GenChat import GenChat

if st.sidebar.button("🔄 Refresh"):
    st.session_state.msg_key = []
    st.session_state.op_key = None

# Initialize session state variables
if msg_key not in st.session_state:
    st.session_state.msg_key = []
if op_key not in st.session_state:
    st.session_state.op_key = None

# Display chat messages from history
for message in st.session_state.msg_key:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if query := st.chat_input("Ask anything..."):
    # Add user message to chat history
    st.session_state.msg_key.append({"role": "user", "content": query})

    # Display user message
    with st.chat_message("user"):
        st.markdown(f"***Question:*** {query}")

    # Process Q&A query
    try:
        response_placeholder = st.empty()
        response_placeholder.info("Loading...")
        response = GenChat().chat(query)
    except Exception as e:
        response = f"There was an error while processing your request: {e}"

    finally:
        # Clear input field
        st.session_state.doc_id = None

    # Display assistant's response
    with st.chat_message("assistant"):
        # Clear the response placeholder
        response_placeholder.empty()
        st.markdown(f"***Answer:*** {response}")

    # Add assistant response to chat history
    st.session_state.msg_key.append({"role": "assistant", "content": response})

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
