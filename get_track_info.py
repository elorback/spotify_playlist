import requests
import json
cid="0f8d056acab64d9d88e4c8892d76d04c"
sec="1c6c19e2d40745988b767e908b8e9508"
def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
    "Content-Type": "application/x-www-form-urlencoded"
    }
    data = { "grant_type":"client_credentials",
            "client_id":"0f8d056acab64d9d88e4c8892d76d04c",
            "client_secret":"1c6c19e2d40745988b767e908b8e9508"
        
    }
    try:
        response = requests.post(url=url,headers=headers,data=data)
        data=response.json()
        token=data['access_token']
    except Exception as e:
        print(e)
    return token
    

access_token = get_access_token()

def get_track_id(artist:str,song_title:str):
    song = song_title.strip()
    artist=artist.strip()
    token = get_access_token()
    headers= {
        "Authorization" : f'Bearer {token}',
        "Content-Type" :"application/json"
    }
    url = 'https://api.spotify.com/v1/search'
    params={
        'q': f'track:{song} artist:{artist}',
        'type':'track',
        'limit':1}
    try:
        
        response = requests.get(url=url,headers=headers,params=params)
        if response.status_code != 200:
            print(f'error: {response.status_code} : {response.text}')
            return
        res_data=response.json()
        pretty = json.dumps(res_data['tracks']['items'][0].get("id"),indent=3)
        return pretty
        
    except Exception as e:
        print(e)

def get_track_attributes(track_id:str):
    pass
    
    
artist=input("artist: ")
title=input("song title: ")
track_id=get_track_id(artist=artist,song_title=title)
print(track_id)