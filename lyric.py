import requests
import time
from bs4 import BeautifulSoup

#TOKEN below should be the string that the API docs tells you
base_url = "http://api.genius.com"
headers = {'Authorization': 'Bearer OtlAODRzS0K0gCnNYGGj1yLOUwXmmfKGadcvkFNFuu_HoOELT_nOKaUAO2fE3eEg'}
search_url = base_url + "/search"

def lyrics_from_song_api_path(song_api_path):
  song_url = base_url + song_api_path
  response = requests.get(song_url, headers=headers)
  json = response.json()
  path = json["response"]["song"]["path"]
  #gotta go regular html scraping... come on Genius
  page_url = "http://genius.com" + path
  page = requests.get(page_url)
  html = BeautifulSoup(page.text, "html.parser")
  #remove script tags that they put in the middle of the lyrics
  [h.extract() for h in html('script')]
  #at least Genius is nice and has a tag called 'lyrics'!
  lyrics = html.find("div", class_="lyrics").get_text() #updated css where the lyrics are based in HTML
  return lyrics

def lyrics_from_genius(song_title, artist_name):
    match = False
    search_url = base_url + "/search"
    data = {'q': song_title}
    response = requests.get(search_url, params=data, headers=headers)
    json = response.json()
    song_info = None
    for hit in json["response"]["hits"]:
        if hit["result"]["primary_artist"]["name"] == artist_name:
            song_info = hit
            match = True
            break
    if match:
        song_api_path = song_info["result"]["api_path"]
        text0 = lyrics_from_song_api_path(song_api_path)
        text1 = text0.replace('\n', ' ')
        text2 = text1.replace('[', ' ')
        text = text2.replace(']', ' ')
        return text
    else:
        return False
