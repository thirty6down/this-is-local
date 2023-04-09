import json
import music_tag
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
from pprint import pprint
import re
import traceback
from itertools import chain

#Config
client_id = ""
client_secret = ""

totalItems = 0
matchedItems = 0
directory = "Music/"
subfolders = [ f.name for f in os.scandir(directory) if f.is_dir() ]

# Clear missing.txt 

missing = open("missing.txt", "w")
missing.write("")
missing.close()

for folder in subfolders:
    try:
        print(folder)
        artistName = folder
        m3ucontents = ""

        from pathlib import Path
        # Create an array of the local library
        localLibrary = []
        flacList = Path(directory + artistName).rglob('*.flac')
        mp3List = Path(directory + artistName).rglob('*.mp3')
        pathlist = chain(flacList, mp3List)
        for path in pathlist:
            # because path is object not string
            path_in_str = str(path)
            #print(path_in_str)
            trackInfo = {
            "Title": None,
            "Album": None,
            "Artist": None
            }

            f = music_tag.load_file(path_in_str)

            # dict access returns a MetadataItem
            trackInfo['Title'] = str(f['title'])
            trackInfo['Album'] = str(f['album'])
            trackInfo['Artist'] = str(f['artist'])
            trackInfo['Path'] = str(path_in_str)
            localLibrary.append(trackInfo)

        #Authentication - without user
        client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
        sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

        search_str = 'This is ' + artistName
        result = sp.search(search_str, 1,0, 'playlist')
        thisisID = (result['playlists']['items'][0]['id'])

        spotifyArray = []
        playlist_id = 'spotify:playlist:' + thisisID
        results = sp.playlist(playlist_id)
        for item in results['tracks']['items']:
            spotifyArray.append({"Title": item["track"]["name"], "Album": item["track"]["album"]["name"]})

        for spotifyTrack in spotifyArray:
            totalItems += 1
            break_loop = False
            for localTrack in localLibrary:
                if re.sub('\W+','', spotifyTrack["Title"].lower()) == re.sub('\W+','', localTrack["Title"].lower()):
                    print("Found match!" + localTrack['Path'])
                    matchedItems += 1
                    m3ucontents += localTrack['Path'].replace(directory + folder +"/", "") + "\n"
                    break_loop = True
                    break
            if break_loop == False:
                print("No match found for " + spotifyTrack["Title"])
                missingtxt = folder + " - " + spotifyTrack["Album"] + " - " + spotifyTrack["Title"] + "\n"
                missing = open("missing.txt", "a")
                missing.write(missingtxt)
                missing.close()

        #make the m3u file

        f = open(directory + "/" + folder + "/" + search_str + ".m3u", "w")
        f.write(m3ucontents)
        f.close()
    except Exception:
        traceback.print_exc()

print("Finished, matched " + str(matchedItems) + "/" + str(totalItems))