import sys

import json
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
#.decoder import JSONDecode

def users_top_tracks(username):
    #username = 22gkfie5pgkyn5ect6h3nixji for my account
    scope = 'user-top-read'
    token = util.prompt_for_user_token(username, scope)
    #'short_term' is 4 weeks, 'medium_term' is 6 months, 'long_term' years???
    range = 'medium_term'
    tracks = []

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        result = sp.current_user_top_tracks(time_range = range, limit = 50)
        for item in enumerate(result['items']):
            track_name = item[1]['name']
            artist_name = item[1]['artists'][0]['name']
            data = (track_name, artist_name)
            tracks.append(data)

    return tracks

def playlist_tracks(uri):
    tracks = []
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    username = uri.split(':')[2]
    playlist_id = uri.split(':')[4]
    results = sp.user_playlist(username, playlist_id,fields='tracks,name')
    for item in enumerate(results['tracks']['items']):
    #    print(json.dumps(item, indent=4, sort_keys=True))
        track_name = item[1]['track']['name']
        artist_name = item[1]['track']['artists'][0]['name']
        data = (track_name, artist_name)
        tracks.append(data)
    return tracks
