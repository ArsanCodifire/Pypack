import streamlit as st
from streamlit_monaco import st_monaco
import requests
import time

# Set up your Discord app credentials
CLIENT_ID = st.secrets["id"]
CLIENT_SECRET = st.secrets["secret"]
REDIRECT_URI = 'https://pypack.streamlit.app'  # Your redirect URI
TOKEN_URL = 'https://discord.com/api/oauth2/token'
USER_URL = 'https://discord.com/api/users/@me'

st.set_page_config(
    page_title="Pypack",
    page_icon="🤖"
)
# Function to get the authorization URL
def get_auth_url():
    return f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=identify email"

# Function to capture the authorization code
def capture_auth_code():
    code=st.query_params.get_all("code")
    if code:
        st.session_state.auth_code = code[0]  # Save the first code

# Call the function to capture the code when the app loads
capture_auth_code()

# Function to determine if the token has expired
def token_has_expired():
    if 'expires_at' in st.session_state:
        return time.time() > st.session_state.expires_at
    return True

# Function to get access and refresh tokens
def get_access_token(auth_code=None, refresh_token=None):
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'scope': 'identify email',
    }

    if auth_code:
        # If we have an auth code, we do the initial token exchange
        data.update({
            'grant_type': 'authorization_code',
            'code': auth_code,
        })
    elif refresh_token:
        # If we have a refresh token, we refresh the access token
        data.update({
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        })

    response = requests.post(TOKEN_URL, data=data)
    token_data = response.json()

    # Save new access and refresh tokens in session state
    st.session_state.access_token = token_data.get('access_token')
    st.session_state.refresh_token = token_data.get('refresh_token')
    st.session_state.expires_in = token_data.get('expires_in')

    # Calculate and store the exact expiry time
    st.session_state.expires_at = time.time() + token_data.get('expires_in')

    return st.session_state.access_token

# Function to get user info
def get_user_info(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(USER_URL, headers=headers)
    return response.json()

# Streamlit UI
st.title("PyPack")
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

# If there is no auth code, show the authorization button
if 'auth_code' not in st.session_state:
    auth_url = get_auth_url()
    st.link_button("Authorize", auth_url)
else:
    # Check if the access token is available and still valid
    if 'access_token' not in st.session_state or token_has_expired():
        if 'refresh_token' in st.session_state:
            access_token = get_access_token(refresh_token=st.session_state.refresh_token)
        else:
            access_token = get_access_token(auth_code=st.session_state.auth_code)
    else:
        access_token = st.session_state.access_token

    if access_token:
        # Retrieve user info after authorization
        user_info = get_user_info(access_token)

        # Create a container for displaying user info
        box = st.container(height=300,border=True)
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_info['id']}/{user_info['avatar']}.png"
        
        # Display the user info and profile picture
        box.title("Dashboard")
        box.image(avatar_url, width=100)  # Display profile picture
        box.write(f"Username: {user_info['username']}")
        
        # Toggle for showing/hiding email
        censor_email = st.toggle("Censor Email", value=True)
        if censor_email:
            box.write("Email Hidden")
        else:
            box.write(f"Email: {user_info.get('email', 'No email returned')}")
        code_box=st_monaco(
            value="",
            height="200px",
            language="python",
            lineNumbers=True,
            minimap=False,
            theme="vs-dark",
        )
        st.title("Coding")
        if st.button("Get content"):
            st.markdown(f"```python{code_box}")
        form=st.form("form", border=True)
        form.title("Send to me")
        form.text_input("Title")
        form.text_area("Content/Body")
        st.form_submit_button("Submit")
    else:
        st.write("Failed to retrieve access token.")
