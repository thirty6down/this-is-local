# this-is-local
## Description
A small script to match a local music collection to spotify's "this is" playlists. Outputs relative .m3u playlists, and a file named "missing.txt" showing any songs not currently in your library. 

## Requirements
- Python
- Spotify API access (sign up at https://developer.spotify.com )
- A local music collection, stored with the structure /Artist/Album/Song.mp3/flac

## Usage
1. Clone/Download the git repo.
2. pip install requirements.txt
3. Open this-is-local.py and put your spotify details into variables client_id & client_secret. Change your "directory" to your music location if needs be.
3. run this-is-local.py

## Known Limitations
- This works best with a well tagged music collection. Take a look at [beets](https://beets.io/) for a simple enough way to set this up
