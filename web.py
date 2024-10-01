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
        background-size: cover; /* Ensure the image covers the entire area */
        background-repeat: no-repeat; /* Prevent repeating the image */
        background-position: center; /* Center the image */
        height: 100vh; /* Full height */
        color: white; /* Adjust text color for better visibility */
    }}

    /* Additional CSS for mobile responsiveness */
    @media only screen and (max-width: 600px) {{
        .stApp {{
            background-size: contain; /* Make the image fit within the viewport */
            height: auto; /* Allow height to adjust */
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)
