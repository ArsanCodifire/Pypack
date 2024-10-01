import streamlit as st
import webbrowser
st.title("Pypack")
image_url = "https://raw.githubusercontent.com/ArsanCodifire/Pypack/refs/heads/main/bg.png"
auth_url="https://discord.com/oauth2/authorize?client_id=1290358916886298769&permissions=8&response_type=code&redirect_uri=https%3A%2F%2Fpypack.streamlit.app&integration_type=0&scope=identify+bot"
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
def log():
    webbrowser.open_new_tab(auth_url)
clk=st.button("Authorise",on_click=log())
