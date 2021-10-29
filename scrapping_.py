import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint


# https://genius.com/api/artists/835/songs/search?page=1&q=michael+jackson&sort=popularity
# https://genius.com/api/artists/41749/songs?page=1&sort=popularity

def get_all_songs_url():
    next_page = 1
    urls = ()
    while next_page:
        r = requests.get(f'https://genius.com/api/artists/835/songs/search?page={next_page}&q=michael+jackson&sort=popularityy')
        contenu = r.json().get("response")
        next_page = contenu.get('next_page', "Not found")
        print(next_page)
        urls += tuple(el.get('url') for el in contenu.get('songs'))
    # pprint(urls)
    return urls

# Get all the songs links
# with open("all_songs_links.json", "w") as f:
#         json.dump(get_all_songs_url(), f, indent=4)

# pprint(get_all_songs_url())

def get_all_lyrics(links):
    lyrics_song = ()
    for link in links:
        x = 0
        results = None
        while results == None:
            print(f"trying link number {links.index(link)}")
            song_page = requests.get(link)
            soup = BeautifulSoup(song_page.content, "html.parser")
            results = soup.find(id="lyrics-root")
            x +=1
            if x == 10:
                break
        if x != 10:
            lyrics_song += tuple(el for el in results.stripped_strings if "[" not in el and "]" not in el and el not in ["Share URL", "Copy","Embed"])[:-1]
        # pprint(lyrics_song)
    return lyrics_song

# Get all the lyrics in all the song links   
with open("songs_lyrics.json", "w") as f:
        json.dump(get_all_lyrics(get_all_songs_url()), f, indent=4)

# print(get_all_lyrics(get_all_songs_url()))