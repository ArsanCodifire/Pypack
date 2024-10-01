import streamlit as st
import webbrowser
st.title("Pypack")
image_url = "https://raw.githubusercontent.com/ArsanCodifire/Pypack/refs/heads/main/bg.png"

# CSS to set the background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('{image_url}');
        background-size: cover; /* Ensure the image covers the entire area */
        background-repeat: no-repeat; /* Prevent repeating the image */
        background-position: center; /* Center the image */
        height: 100vh; /* Full height */
        color: white; /* Adjust text color for better visibility */
    }}
    </style>
    """,
    unsafe_allow_html=True
)
