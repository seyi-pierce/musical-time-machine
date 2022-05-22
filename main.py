from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# from pprint import pprint

CLIENT_ID = YOUR CLIENT ID
CLIENT_SECRET = YOUR CLIENT SECRET
REDIRECT_URI = YOUR REDIRECT URI

######################### User's Date of Choice ######################
date_of_choice = input("What year would you like to travel?\nPlease answer using the YYYY-MM-DD format.\n")
year = date_of_choice.split("-")[0]
billboard_url = f"https://www.billboard.com/charts/hot-100/{date_of_choice}/"

######################### Getting Billboard's website information ######################
response = requests.get(url=billboard_url)
response.raise_for_status()
content = response.text

######################### Extracting the top 100 songs ######################
soup = BeautifulSoup(content, "html.parser")
song_list_tags = soup.select("li ul li h3")
song_list = [tag.getText().strip() for tag in song_list_tags]
print(song_list)

######################### Creating an instance of spotify class ######################
spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = spotify.current_user()["id"]

######################### List of Songs URI ######################
playlist_uri = []
for song in song_list:
    result = spotify.search(q=f"track:{song} year:{year}", type="track")
    try:
        song_uri = result["tracks"]["items"][0]["uri"]
        playlist_uri.append(song_uri)
    except IndexError:
        print(f"URI for {song} doesn't exist on Spotify!")
print(playlist_uri)

######################### Creating a Playlist ######################
playlist = spotify.user_playlist_create(
    user=user_id,
    public=False,
    name=f"{date_of_choice} Billboard 100",
    description=f"Top 100 songs on {date_of_choice}. Might be incomplete as not all songs may be available on Spotify."
                             )
playlist_id = playlist["id"]
print(playlist_id)

######################### Adding Songs to playlist ######################
spotify.playlist_add_items(playlist_id=playlist_id, items=playlist_uri)
