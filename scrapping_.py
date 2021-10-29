import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint


# https://genius.com/api/artists/835/songs/search?page=1&q=michael+jackson&sort=popularity
# https://genius.com/api/artists/41749/songs?page=1&sort=popularity

def get_all_songs_url():
    next_page = 1
    urls = []
    while next_page:
        r = requests.get(f'https://genius.com/api/artists/835/songs/search?page={next_page}&q=michael+jackson&sort=popularityy')
        contenu = r.json().get("response")
        next_page = contenu.get('next_page', "Not found")
        print(next_page)
        urls.extend([el['url'] for el in contenu.get('songs')])
    # pprint(urls)
    return urls

# Get all the songs links
# with open("links.json", "w") as f:
#         json.dump(get_all_songs_url(), f, indent=4)

# get_all_songs_url()

def get_all_lyrics(links):
    lyrics_song = []
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
            lyrics_song.extend([el for el in results.stripped_strings if "[" not in el and "]" not in el and el not in ["Share URL", "Copy","Embed"]][:-1])
        # pprint(lyrics_song)
    return lyrics_song

# Get all the lyrics in all the song links   
# with open("songs.json", "w") as f:
#         json.dump(get_all_lyrics(get_all_songs_url()), f, indent=4)

# get_all_lyrics(get_all_songs_url())

#Test using the file
# with open("links.json", "r") as f:
#        les_liens = json.load(f)

# # print(les_liens[367])

# lyrics_song = []
# for link in les_liens[365:369]:
#     x = 0
#     results = None
#     while results == None:
#         print(f"trying link number {les_liens.index(link)}")
#         song_page = requests.get(link)
#         soup = BeautifulSoup(song_page.content, "html.parser")
#         results = soup.find(id="lyrics-root")
#         x +=1
#         if x == 10:
#             break
#     if x != 10:
#         lyrics_song.extend([el for el in results.stripped_strings if "[" not in el and "]" not in el and el not in ["Share URL", "Copy","Embed"]][:-1])
# pprint(lyrics_song)