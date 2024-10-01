import streamlit as st
import webbrowser
st.title("Pypack")
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHBKD9aKNPZI-BLkZUoHCRLGSsBXXHPRgfU1JpLpgyA99YHjOdi3cGG2Wk&s=10"

# CSS to set the background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('{image_url}');
        background-size: cover;
        background-position: center;
        height: 100vh;
        color: white;  /* Adjust text color for better visibility */
    }}
    </style>
    """,
    unsafe_allow_html=True
)
