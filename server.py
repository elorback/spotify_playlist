



from flask import Flask, request, redirect, session
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session storage


SCOPE = "user-top-read"  # or any scope you need
CLIENT_ID = "0f8d056acab64d9d88e4c8892d76d04c"
CLIENT_SECRET = "1c6c19e2d40745988b767e908b8e9508"
REDIRECT_URI = 'http://127.0.0.1:8000/callback'


sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    show_dialog=True,
)

@app.route("/")
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    error = request.args.get("error")

    if error:
        return f"Spotify Authorization Error: {error}"

    token_info = sp_oauth.get_access_token(code)
    t=sp_oauth.get_cached_token()
    access_token = token_info["access_token"] if isinstance(token_info, dict) else token_info


    if not token_info:
        return "Could not get access token."

    access_token = token_info["access_token"]
    print(f"access token: {access_token}")

    # Save token in session or use it directly
    session["token_info"] = token_info

    # Use token to create Spotify client
    sp = Spotify(auth_manager=sp_oauth)

    # Example: Get audio features for a hardcoded track
    track_id = "7LRMbd3LEoV5wZJvXT1Lwb"
    try:
        features = sp.audio_features([track_id])
        return f"<pre>{features}</pre>"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(debug=True,port=8000)
