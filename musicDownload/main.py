import os
import requests


def download_music(music_url: str, music_name: str, gender):
    r = requests.get(music_url, allow_redirects=True)
    try:
        open(f'../Music/{gender}/{music_name.replace(" ", "_")}.mp3', 'wb')\
            .write(r.content)
    except FileNotFoundError:
        os.mkdir(f'../Music/{gender}/')
        download_music(music_url, music_name, gender)


def main():
    fuzzy_tags = 'hiphop'
    response = requests.get(
        f'https://api.jamendo.com/v3.0/tracks/'
        f'?client_id=96222e28'
        f'&format=jsonpretty'
        f'&include=musicinfo'
        f'&fuzzytags={fuzzy_tags}'
    )
    results = response.json()['results']
    for music in results:
        if music['audiodownload_allowed']:
            download_music(music['audiodownload'],
                           music['name'],
                           fuzzy_tags)


if __name__ == '__main__':
    main()
