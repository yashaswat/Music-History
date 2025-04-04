from dotenv import load_dotenv
import os
import json
from requests import get, post
import base64

load_dotenv()

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')


def get_token():
    
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_b64 = str(base64.b64encode(auth_bytes), 'utf-8')
    
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_b64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    
    token = json_result['access_token']
    return token


def get_auth_header(token):
    return {'Authorization': 'Bearer ' + token}


def search_for_artist(token, artist_name):

    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    
    if len(json_result) == 0:
        print('No artist found')
        return None
    
    return json_result[0]

def get_song_from_artist(token, artist_id):
    
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=IN"
    headers = get_auth_header(token)
    
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result


def get_user_playlists(token, user_id):

    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = get_auth_header(token)
    
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['items']
    
    return json_result    

def get_playlist(token, playlist_id):
    
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?fields=items(track(name, album(name)))"
    headers = get_auth_header(token)
    
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['items']
    
    return json_result
    
if __name__ == '__main__':
    
    api_token = get_token()
    user_id = 'pv5iaq3dsw5k7r6edmqcbqlpe'

    playlists = get_user_playlists(api_token, user_id)
    for i, playlist in enumerate(playlists):
        print(f"{i+1}. {playlist['name']} ({playlist['id']})")

    playlist_songs = get_playlist(api_token, '5Gv8Z2HSDjGY9tSmqpuxUv')
    print('\n------------------------------------------------\n')
    for i, playlist in enumerate(playlist_songs):
        print(f"{i+1}. {playlist['track']['name']} ({playlist['track']['album']['name']})")
    print('\n------------------------------------------------\n')
        
    # artist_data = search_for_artist(api_token, 'Nanku')
    # artist_id = artist_data['id']

    # top_tracks = get_song_from_artist(api_token, artist_id)

    # for i, track in enumerate(top_tracks):
    #     print(f"{i+1}. {track['name']}")
