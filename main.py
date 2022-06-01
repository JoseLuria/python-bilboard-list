from functions import spotify_aut
from classes import SongsList


def run():
    spotify = spotify_aut()
    user_id = spotify.current_user()["id"]
    run_loop = True

    while run_loop:
        date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
        print(f"Your user ID is {user_id}")

        song_list = SongsList(date, spotify)

        song_list_exist = song_list.get_songs(user_id)

        if song_list_exist:
            run_loop = False

            song_list.write_document()

            print("File with songs created")
        else:
            print("Sorry that year is incorrect")


if __name__ == "__main__":
    run()
