import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

# date = input("Enter the date to travel to (YYYY-MM-DD): \n>")

date = "2002-12-02"
year = 2002



response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/", headers=header)

soup = BeautifulSoup(response.text, "html.parser")

artist_scrap = soup.select(
    selector="body .pmc-paywall .o-chart-results-list-row-container ul .lrv-u-width-100p ul li span", _class="c-label")

# SCRAPING
song_scrap = soup.select(
    selector="body .pmc-paywall .o-chart-results-list-row-container ul .lrv-u-width-100p ul li h3")

songs = [" ".join(song.getText().split()) for song in song_scrap]

art_list = [" ".join(artist.getText().split()) for artist in artist_scrap]

art_list = art_list[::7]

for i, (art, song) in enumerate(zip(art_list, songs)):
    print(f"{i:2}: {art:46}: {song}")


SPOTIPY_CLIENT_ID = "..."
SPOTIPY_CLIENT_SECRET = "..."
SPOTIPY_REDIRECT_URI = "http://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=SPOTIPY_REDIRECT_URI,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="...",
    )
)
user_id = sp.current_user()["id"]

uri_list = []
for title, artist in zip(songs, art_list):
    query = f"track:{title}, artist:{artist} year:{year}"
    response = sp.search(q=query, limit=1, type="track")
    try:
        uri_list.append(response['tracks']['items'][0]['uri'])
    except IndexError:
        pass

playlist = sp.user_playlist_create(user="...", name="name_of_playlist",
                                   public=False)
playlist_id = playlist["id"]

sp.playlist_add_items(playlist_id=playlist["id"], items=uri_list)
