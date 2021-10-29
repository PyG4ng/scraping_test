import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint


# https://genius.com/api/artists/835/songs/search?page=1&q=michael+jackson&sort=popularity
# https://genius.com/api/artists/41749/songs?page=1&sort=popularity

def get_all_songs_url():
    next_page = 1
    urls = []
    while next_page <= 10:
        r = requests.get(f'https://genius.com/api/artists/835/songs/search?page={next_page}&q=michael+jackson&sort=popularityy')
        contenu = r.json().get("response")
        next_page = contenu.get('next_page', "Not found")
        print(next_page)
        urls.extend([el['url'] for el in contenu.get('songs')])
    # pprint(urls)
    return urls

def get_all_lyrics(links):
    lyrics_song = []
    for link in links:
        results = None
        while results == None:
            print(f"trying link number {links.index(link)}")
            song_page = requests.get(link)
            soup = BeautifulSoup(song_page.content, "html.parser")
            results = soup.find(id="lyrics-root")
        lyrics_song.extend([el for el in results.stripped_strings if "[" not in el and "]" not in el and el not in ["Share URL", "Copy","Embed"]][:-1])
        # pprint(lyrics_song)
    with open("songs.json", "w") as f:
        json.dump(lyrics_song, f, indent=4)

get_all_lyrics(get_all_songs_url())