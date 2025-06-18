from flask import Flask, request, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

CLIENT_ID = "0f8d056acab64d9d88e4c8892d76d04c"
CLIENT_SECRET = "1c6c19e2d40745988b767e908b8e9508"
REDIRECT_URI = 'https://127.0.0.1:8000/callback'

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
)

@app.route("/")
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get('code')
    error = request.args.get('error')

    if error:
        return f"Error: {error}"

    # Exchange the code for an access token
    token_info = sp_oauth.get_access_token(code=code)

    if not token_info:
        return "Failed to get access token. Try logging in again."

    access_token = token_info['access_token']  # In recent spotipy versions, get_access_token returns token string directly
    print(access_token)
    sp = spotipy.Spotify(auth=access_token)
    features=None
    track_id = "7LRMbd3LEoV5wZJvXT1Lwb"  # Replace with any track id
    try:
        features = sp.audio_features([track_id])
        print(features)
    except Exception as e:
        print(e)
        print(features)
    return features


if __name__ == "__main__":
    app.run(debug=True, port=8000)
