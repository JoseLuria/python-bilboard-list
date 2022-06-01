import os
import spotipy
from dotenv import load_dotenv
from spotipy import SpotifyOAuth


def format_text(text):
    """Remove all the \n  and \t elements in a string"""
    remove_salt = text.replace("\n", "")
    return remove_salt.replace("\t", "")


def spotify_aut():
    """Return the authentication object from spotipy"""
    load_dotenv()

    client_id = os.getenv("SECRET_ID")
    client_secret = os.getenv("SECRET_CLIENT")

    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="https://www.spotify.com/mx/",
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt"
    ))


def get_spotify_uri(spotify, song, artist):
    """Return the Spotify uri of the son if exist in the son not exist return None"""
    search_result = spotify.search(q=f"track:{song} artist:{artist}", limit=1, offset=0, type="track")
    tracks = search_result["tracks"]["items"]

    if len(tracks) > 0:
        return tracks[0]["uri"]

    print(f"{song} is not available in spotify")
    return None


def create_playlist(spotify, date, user_id):
    """Create a new Spotify playlist and return the playlist id"""
    playlist_name = f"{date} Billboard 100"
    new_playlist = spotify.user_playlist_create(user=user_id, name=playlist_name, public=False)
    print(f"\nPlaylist {playlist_name} created\n")

    return new_playlist["id"]
