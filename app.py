from flask import Flask, request, render_template
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import urllib.parse
import requests
import requests.exceptions
import os

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", "")


app = Flask(__name__)


# Initiera Spotipy
sp = Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    url = request.form.get('spotify_url')
    if not url:
        return "Ingen URL mottagen", 400

    try:
        # Om det är en hitsternordics-länk, följ redirect
        if 'hitsternordics' in url:
            print("Försöker följa redirect till:", url)
            try:
                response = requests.get(url, allow_redirects=True, timeout=5)
                url = response.url
            except requests.exceptions.RequestException as e:
                return f"Fel vid hämtning av URL: {str(e)}", 500

        # Extrahera Spotify-ID
        track_id = url.split("/")[-1].split("?")[0]
        track = sp.track(track_id)
        title = track['name']
        artist = track['artists'][0]['name']

        # Skapa YouTube Music-sökning
        query = urllib.parse.quote(f"{title} {artist}")
        youtube_url = f"https://music.youtube.com/search?q={query}"

        # Returnera sök-URL som text (ej redirect)
        return youtube_url

    except Exception as e:
        return f"Fel: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

