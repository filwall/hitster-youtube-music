from flask import Flask, request, render_template, jsonify
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import urllib.parse
import requests
import requests.exceptions
import os
import re
import json

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", "")
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "")

app = Flask(__name__)

# Initiera Spotipy
sp = Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

@app.route('/')
def index():
    return render_template('index.html')

def search_youtube(query):
    """Search YouTube for a specific song and return the video ID of the best match"""
    if not YOUTUBE_API_KEY:
        return None
        
    try:
        # Add "topic" to search query to prioritize official artist channels
        search_query = f"{query} topic"
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={urllib.parse.quote(search_query)}&type=video&key={YOUTUBE_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            return data['items'][0]['id']['videoId']
        return None
    except Exception as e:
        print(f"YouTube API error: {str(e)}")
        return None

@app.route('/convert', methods=['POST'])
def convert():
    url = request.form.get('spotify_url')
    if not url:
        return jsonify({"error": "Ingen URL mottagen"}), 400

    try:
        # Om det är en hitsternordics-länk, följ redirect
        if 'hitsternordics' in url:
            print("Försöker följa redirect till:", url)
            try:
                response = requests.get(url, allow_redirects=True, timeout=5)
                url = response.url
            except requests.exceptions.RequestException as e:
                return jsonify({"error": f"Fel vid hämtning av URL: {str(e)}"}), 500

        # Extrahera Spotify-ID
        track_id = url.split("/")[-1].split("?")[0]
        track = sp.track(track_id)
        title = track['name']
        artist = track['artists'][0]['name']
        
        # Kombinera för sökning
        full_query = f"{title} {artist}"
        
        # Försök hitta en exakt video-ID med YouTube API om API-nyckeln finns
        video_id = search_youtube(full_query)
        
        # Om vi hittar ett video-ID, skapa en direkt länk utan autoplay parameter
        # (vi hanterar detta på klientsidan nu)
        if video_id:
            # Använd YouTube Music-formatet med videoId
            youtube_url = f"https://music.youtube.com/watch?v={video_id}"
        else:
            # Fallback till sökning om vi inte har API-nyckel eller inget resultat hittades
            query = urllib.parse.quote(f'"{title}" "{artist}"')
            youtube_url = f"https://music.youtube.com/search?q={query}"
        
        return jsonify({
            'youtube_url': youtube_url,
            'title': title,
            'artist': artist,
            'direct_link': video_id is not None
        })

    except Exception as e:
        return jsonify({"error": f"Fel: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
