## Note

This app is currently under development and does **not** support music autoplay by default.

To use the app, you will need to provide your own **Spotify Client ID** and **Client Secret**.

You can obtain these by visiting [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)  
and creating a new application. Once created, your Client ID and Secret will be available in the app settings.

### Optional: YouTube API Key (Recommended)

Providing a **YouTube API Key** is optional but highly recommended, especially if you want autoplay to work.

To obtain a YouTube API Key:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Enable the **YouTube Data API v3** for your project.
4. Generate an API key from the **Credentials** section.

### About Autoplay

Autoplay will function **only if**:
- You have **YouTube Music installed**, or
- You are using a supported browser like **Firefox** or **Chrome**, **and** you’ve provided a valid YouTube API key.

If no API key is provided, the app will search for the track, but **you’ll need to press play manually**.

