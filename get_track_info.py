import requests
import json
from spotipy import SpotifyOAuth,Spotify
CLIENT_ID = "0f8d056acab64d9d88e4c8892d76d04c"
CLIENT_SECRET = "1c6c19e2d40745988b767e908b8e9508"

def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        print(f"Token request failed: {response.status_code} - {response.text}")
        return None
    return response.json()["access_token"]

def get_track_id(artist, title, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": f"track:{title} artist:{artist}",
        "type": "track",
        "limit": 1
    }
    url = "https://api.spotify.com/v1/search"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Search request failed: {response.status_code} - {response.text}")
        return None
    data = response.json()
    items = data.get('tracks', {}).get('items', [])
    if not items:
        print("No track found.")
        return None
    return items[0]['id']

def get_audio_features(track_id):
    
    sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://127.0.0.1:8000",))

    try:
        res = sp.audio_features(tracks=[track_id])
        print(res)
    except Exception as e:
        print(e)
# def get_track_by_id(id,token):
#     res=None
#     headers = {"Authorization":f"Bearer {token}"}
#     url= f"https://api.spotify.com/v1/tracks/{id}"
#     try:
#         res = requests.get(url=url,headers=headers)
#         res =res.json()
#         parsed = json.dumps(res,indent=5)
#         #print(parsed)
#         print({res["artists"][0]["name"]:res["name"]})
#     except Exception as e:
#         print(e)
# Main logic
if __name__ == "__main__":
    token=get_access_token()
    artist = input("artist: ")
    track = input("track: ")
    id = get_track_id(artist=artist,title=track,token=token)

    #print(get_track_by_id(id,token=get_access_token()))
    #print(id)
    get_audio_features(id)
