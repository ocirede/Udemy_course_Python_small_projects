import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import datetime as dt


load_dotenv()


uris_list = []

URL = "https://www.billboard.com/charts/hot-100/2000-08-12/"

date = dt.datetime.now().date()
playlist_name = f"{date} Billboard 100"

response = requests.get(url=URL)
billboard = response.text

soup = BeautifulSoup(billboard, "html.parser")

songs = soup.select(".o-chart-results-list__item h3")
artists = soup.select(".o-chart-results-list__item span")

billboard_songs_list = [song.getText(strip=True) for song in songs]
billboard_artists_list = [artist.getText(strip=True) for artist in artists]
filtered_artists_list = [artist for artist in billboard_artists_list if not artist.isdigit() and artist != "-" and artist != "NEW"]

scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id= os.getenv("CLIENT_ID"),
    client_secret= os.getenv("CLIENT_SECRET"),
    redirect_uri= os.getenv("REDIRECT_URI"),
    scope=scope))

user_profile = sp.current_user()
user_id = user_profile["id"]

for song, artist in zip(billboard_songs_list, filtered_artists_list):
    query = f'track:"{song}" artist:"{artist}"'
    results = sp.search(q=query, type="track", limit=1)

    items = results['tracks']['items']
    if items:
        first_track = items[0]
        uris_list.append(first_track['external_urls']['spotify'])
    else:
        print(f"No results found for '{song}' by '{artist}'")

playlist = sp.user_playlist_create(user=user_id,  name=playlist_name, public=False, description="Top 100 from Billboard")
playlist_id = playlist["id"]
sp.playlist_add_items(playlist_id=playlist_id, items=uris_list)





