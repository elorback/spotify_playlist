import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="https://localhost:3000",
    scope="user"
))

track = "Shape of You"
artist = "Ed Sheeran"

results = sp.search(q=f"track:{track} artist:{artist}", type="track", limit=1)
items = results["tracks"]["items"]

if not items:
    print("No track found.")
else:
    track_id = items[0]["id"]
    print("Track ID:", track_id)
    features = sp.audio_features([track_id])[0]
    print("Audio Features:", features)
