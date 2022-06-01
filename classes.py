import requests
import json
from bs4 import BeautifulSoup
from functions import format_text, get_spotify_uri, create_playlist


class SongsList:
    def __init__(self, date, spotify):
        self.date = date
        self.songs = []
        self.songs_uris = []
        self.spotify = spotify

    def get_songs(self, user_id):
        site_html = requests.get(f"https://www.billboard.com/charts/hot-100/{self.date}/")

        if site_html.status_code == 200:
            soup = BeautifulSoup(site_html.text, "html.parser")
            songs_list = soup.findAll(name="div", class_="o-chart-results-list-row-container")

            if len(songs_list) == 0:
                return False

            print("\nCreating your songs list...\n")

            for song_tag in songs_list:
                self.add_song(song_tag)

            playlist_id = create_playlist(self.spotify, self.date, user_id)
            self.spotify.playlist_add_items(playlist_id=playlist_id, items=self.songs_uris)
            print("Songs added to the list\n")
            return True

        return False

    def add_song(self, song):
        song_title_tag = song.find(name="h3", id="title-of-a-story")
        song_band_tag = song.find(name="span", class_="a-no-trucate")

        song_title = format_text(song_title_tag.getText())
        song_band = format_text(song_band_tag.getText())
        song_uri = get_spotify_uri(self.spotify, song_title, song_band)

        if song_uri:
            self.songs_uris.append(song_uri)

        self.songs.append({
            "song": song_title,
            "artist": song_band,
            "uri": song_uri
        })

    def write_document(self, document_indent=2):
        with open("songs.json", "w", encoding="utf-8") as songs_file:
            songs = self.songs
            parsed_songs = json.dumps(songs, indent=document_indent)
            songs_file.write(parsed_songs)
