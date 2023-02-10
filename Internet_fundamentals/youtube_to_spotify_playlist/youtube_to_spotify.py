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


def get_list_of_songs_from_youtube_playlist():
    youtube = get_authenticated_service()

    request = youtube.playlists().list(part="snippet", mine=True)
    response = request.execute()

    list_of_playlist = []    
    for item in response['items']:
        print("Id: ", item['id'])
        print("Title: ", item['snippet']['title'])
        list_of_playlist.append({'name': item['snippet']['title'], 'id': item['id']})

    
    print("Select a playlist")
    for playlist in list_of_playlist:
        print(playlist['name'])

    user_selection = str(input("Type in the playlist name: "))

    pid = ''
    for playlist in list_of_playlist:
        if playlist['name'].lower() == user_selection.lower():
            pid = playlist['id']


    request = youtube.playlistItems().list(part="snippet", playlistId=pid, maxResults=100)
    response = request.execute()

    list_of_songs = []
    for song_name in response['items']:
        #print(song_name['snippet']['title'])
        list_of_songs.append(song_name['snippet']['title'])
    
    return list_of_songs


# Returns a spotify client object
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


def search_spotify(spotify_client, titles_list):
    print('\nSearching....\n')
    add_tracks_id_list = []
    not_found = []

    for title in titles_list:
        print(f'Searching Track: {title}')
        with open('searched.csv', mode='a') as searched_file:
            searched_writer = csv.writer(searched_file)
            searched_writer.writerow([title])
        result = spotify_client.search(
            title, limit=1, offset=0, type='track', market=None)
        if result['tracks']['total'] == 0:
            ntitle = title
            while(len(ntitle) >= 25):
                ntitle = ntitle.rsplit(' ', 1)[0]
                print(f'Searching: {ntitle}')
                result = spotify_client.search(
                    ntitle, limit=1, offset=0, type='track', market=None)
                if result['tracks']['total']:
                    result_id = result['tracks']['items'][-1]['id']
                    add_tracks_id_list.append(result_id)
                    print(f'Track found : {ntitle} ')
                    break
            if result['tracks']['total'] == 0:
                print(f'Not found: {title}')
                not_found.append(title)
        else:
            result_id = result['tracks']['items'][-1]['id']
            add_tracks_id_list.append(result_id)
            print(f'Track found : {title}')
    print(f'\nTotal Tracks searched: {len(titles_list)}')
    # tracks_not_found = len(titles_list) - len(add_tracks_id_list)
    if not_found:
        print(f'{len(not_found)} Tracks not found: {not_found}')
    # print(f'Tracks not found: {tracks_not_found} - {not_found[(len(not_found)-tracks_not_found):]}')
    return add_tracks_id_list


#adds new tracks to the playlist
def add_tracks_spotify(spotify_client, add_tracks_id_list):
    new = []
    for track in add_tracks_id_list:
        track_ = spotify_client.track(track)
        track_name = track_['name']
        artist = track_['album']['artists'][0]['name']
        name = artist + '-' + track_name
        new.append(name)
        print(f'Adding track: {name}')
    if add_tracks_id_list:
        spotify_client.user_playlist_add_tracks(
            SPOTIFY_USERNAME, YOUTUBE_PLAYLIST_ID, add_tracks_id_list, position=0)
        print(f'\n{len(new)} new tracks added: {new}\n')

    else:
        print('\n***************** No new tracks to add! *****************\n')


def check_if_already_exists(youtube_titles):
    unique_tracks = []
    if os.path.isfile(LOCAL_CSV_FILE):
        with open(LOCAL_CSV_FILE, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        
        flat_list = [item for sublist in data for item in sublist]
        print("Data: ", flat_list)
        for title in youtube_titles:
            if title not in flat_list:
                unique_tracks.append(title)
        return unique_tracks
    else:
        return youtube_titles     


if __name__ == "__main__":
    youtube_titles = get_list_of_songs_from_youtube_playlist()
    spotify_client = init_spotify_client()
    updated_tracks = check_if_already_exists(youtube_titles)
    new_tracks = search_spotify(spotify_client, updated_tracks)
    add_tracks_spotify(spotify_client, new_tracks)
