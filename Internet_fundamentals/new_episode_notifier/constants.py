SENDGRID_API_KEY = ''

MOVIE_DB_URL = 'https://api.themoviedb.org/3/discover/tv?api_key=489d17035e3c102567659de6759b8bfd&language=en-US&sort_by=popularity.desc&page=1&timezone=America%2FNew_York&include_null_first_air_dates=false&with_watch_monetization_types=flatrate&with_status=0&with_type=0'

FROM_EMAIL = 'from_email@example.com'
TO_EMAIL = 'to@example.com'
SUBJECT = 'New season/episode is out'

LOCAL_FILE_NAME = "shows_to_track.csv"

FIELDNAMES = ['show_name', 'show_id', 'last_season_watched', 'last_episode_watched']