import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import csv
import spotipy
import spotipy.util as util
import sys
from constants import *
import google


def get_authenticated_service():
    # Disable OAuthlib's HTTPS
	# verification when running locally.
	# *DO NOT* leave this option
	# enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    try:
        credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(CLIENT_SECRET_FILE, GSCOPES)
    except ValueError as e:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, GSCOPES)
        credentials = flow.run_console()
        with open(CLIENT_SECRET_FILE, 'w') as file:
            file.write(credentials.to_json())
    return googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)



def init_spotify_client():
    try:
        print('Initialising Spotify Client....')
        token = util.prompt_for_user_token(SPOTIFY_USERNAME, SCOPE,
                                           client_id=CLIENT_ID,
                                           client_secret=CLIENT_SECRET,
                                           redirect_uri=REDIRECT_URI)
        spotify_client = spotipy.Spotify(auth=token)
        print('\nClient initialised!\n')
        return spotify_client
    except:
        sys('\nError initialising Spotify Client!\n')


def get_list_of_user_playlists(user_playlists_object):
    user_playlists_list = []
    for playlist in user_playlists_object['items']:
        user_playlists_list.append({'name': playlist['name'], 'id': playlist['id']})
    return user_playlists_list  


def remove_already_existing_tracks(track_names):
    previously_added_tracks = []
    if os.path.exists(LOCAL_FILE):
        with open(LOCAL_FILE) as file:
            previously_added_tracks = [line.rstrip() for line in file]
    else:
        f = open(LOCAL_FILE, "x")     
        f.close()   

    if previously_added_tracks:
        for track in previously_added_tracks:
            if track in track_names:
                track_names.remove(track)

    return track_names            


def add_to_youtube_playlist(youtube_obj, playlist_id, track_names):
    for track in track_names:
        request = youtube_obj.search().list(part="snippet", q=track)
        response = request.execute()

        video_id = response['items'][0]['id']['videoId']
        add_video_request = youtube_obj.playlistItems().insert(
        part="snippet",
        body={
                'snippet': {
                'playlistId': playlist_id, 
                'resourceId': {
                        'kind': 'youtube#video',
                    'videoId': video_id
                    }
                #'position': 0
                }
        }).execute()

    if track_names:
        print("Tracks added to playlist Successfully")

        with open(LOCAL_FILE, 'a') as f:
            for line in track_names:
                f.write(f"{line}\n")
    else:
        print("No new tracks to add!!!!!")            


def get_youtube_playlists(track_names):
	
	# Disable OAuthlib's HTTPS
	# verification when running locally.
	# *DO NOT* leave this option
	# enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    youtube = get_authenticated_service()
    request = youtube.playlists().list(part="snippet", mine=True)
    response = request.execute()

    list_of_playlist = []    
    for item in response['items']:
        list_of_playlist.append({'name': item['snippet']['title'], 'id': item['id']})

    print("Select a youtube playlist you'd like to add songs to")
    for playlist in list_of_playlist:
        print(playlist['name'])

    user_selection = str(input("Type in the playlist name: "))

    pid = ''
    for playlist in list_of_playlist:
        if playlist['name'].lower() == user_selection.lower():
            pid = playlist['id']

    updated_track_names = remove_already_existing_tracks(track_names)
    add_to_youtube_playlist(youtube, pid, updated_track_names)


def get_track_names(playlist_data):
    tracks_names_list = []
    for item in playlist_data['items']:
        print(item['track']['name'])
        tracks_names_list.append(item['track']['name'] + " by " + item['track']['artists'][0]['name'])

    return tracks_names_list


if __name__ == "__main__":
    spotify_client = init_spotify_client()

    user_playlists = spotify_client.current_user_playlists(limit=50, offset=0)
    playlists_list = get_list_of_user_playlists(user_playlists)

    for playlist in playlists_list:
        print(playlist['name'])

    user_selection = str(input("Select a spotify playlist you want to add songs from: "))  

    pid = ''
    for playlist in playlists_list:
        if playlist['name'].lower() == user_selection.lower():
            pid = playlist['id']
            print("pid: ", pid)

    playlist_data = spotify_client.playlist_tracks(playlist_id=pid)

    track_names = get_track_names(playlist_data)

    get_youtube_playlists(track_names)

    





