import streamlit as st
import requests
import streamlit.components.v1 as components
import os

# Set up your Discord app credentials
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDIRECT_URI = 'https://pypack.streamlit.app'  # Your redirect URI
TOKEN_URL = 'https://discord.com/api/oauth2/token'
USER_URL = 'https://discord.com/api/users/@me'

# Function to get the authorization URL
def get_auth_url():
    return f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify email"

# Streamlit UI
st.title("Pypack")
image_url = "https://raw.githubusercontent.com/ArsanCodifire/Pypack/refs/heads/main/bg.png"
# CSS to set the background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('{image_url}');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        height: 100vh;
        color: white;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

if 'auth_code' not in st.session_state:
    auth_url=get_auth_url()
    st.link_button("Authorise.", auth_url)
else:
    # Retrieve user info after authorization
    access_token = get_access_token(st.session_state.auth_code)
    if access_token:
        user_info = get_user_info(access_token)
        st.title("Dashboard")
        st.write(f"Username: {user_info['username']}")
        st.write(f"Email: {user_info.get('email', 'No email returned')}")
    else:
        st.write("Failed to retrieve access token.")

# Component to capture the authorization code from the URL
def capture_auth_code():
    code = st.experimental_get_query_params().get("code", [None])[0]
    if code:
        st.session_state.auth_code = code

# Call the function to capture the code when the app loads
capture_auth_code()

def get_access_token(auth_code):
    response = requests.post(TOKEN_URL, data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'scope': 'identify email'
    })
    return response.json().get('access_token')

def get_user_info(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(USER_URL, headers=headers)
    return response.json()
    
