import streamlit as st
import webbrowser
import requests

# Discord OAuth2 Configuration
client_id = "YOUR_CLIENT_ID"  # Replace with your Discord client ID
client_secret = "YOUR_CLIENT_SECRET"  # Replace with your Discord client secret
redirect_uri = "http://localhost:8501"  # Change based on your app setup
auth_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=identify%20email"
token_url = "https://discord.com/api/oauth2/token"
user_info_url = "https://discord.com/api/users/@me"

# App title
st.title("Pypack")

# Button to start authorization
if st.button("Login with Discord"):
    webbrowser.open_new_tab(auth_url)
    st.write("Please complete the login and return to the app.")

# Once user authorizes, they will be redirected with a code
code = st.text_input("Enter the authorization code here after login:")

# Exchange authorization code for access token
if code:
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Request access token
    response = requests.post(token_url, data=data, headers=headers)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        
        # Use the access token to get user info
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        user_info = requests.get(user_info_url, headers=headers).json()
        
        # Display user info
        st.write(f"Logged in as: {user_info['username']}")
        st.write(f"Email: {user_info['email']}")
    else:
        st.write("Failed to retrieve access token.")
        