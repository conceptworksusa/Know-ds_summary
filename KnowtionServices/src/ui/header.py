import streamlit as st

def show_sidebar_logo(title: str):
    # Sticky header style
    st.markdown(rf"""
        <style>
        .fixed-header {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background-color: white;
            z-index: 9999;
            padding: 10px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .spacer {{
            margin-top: 80px; /* Push content down to avoid overlap */
        }}
        </style>
        <div class="image-container">
            <img src="C:\Users\skarnatapu\source\repos\Knowtion-ds_summary\KnowtionServices\src\ui\logo.png" alt="Image Description" />
        </div>
        <div class="fixed-header">
            <img src="C:\Users\skarnatapu\source\repos\Knowtion-ds_summary\KnowtionServices\src\ui\logo.png">
            <h2>💬{title}</h2>
        </div>
        <div class="spacer"></div>
    """, unsafe_allow_html=True)
    # st.sidebar.image(r"C:\Users\skarnatapu\source\repos\Knowtion-ds_summary\KnowtionServices\src\ui\logo.png", width=500)

