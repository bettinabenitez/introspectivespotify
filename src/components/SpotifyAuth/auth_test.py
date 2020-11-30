import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import SpotifyAuth.SpotifyAuth as SpotifyAuth

# DB imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from SpotifyAuth.database_setup import Base, User

load_dotenv()

# connect to IntrospectiveSpotify database
DB_STRING = os.getenv("DB_STRING")
engine = create_engine(DB_STRING)
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
db_session = Session()


# instantiate spotify object
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
scope = "user-read-recently-played, user-top-read, user-read-playback-position, user-read-playback-state, user-modify-playback-state, user-read-currently-playing, playlist-modify-public, user-read-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            redirect_uri=REDIRECT_URI,
                            scope=scope, cache_path=".oAuthCache"))

# BLACK BOX TESTS
async def test_login(bot, user):
    pass

def test_logout(user):
    pass

def test_get_token(user):
    return_string = "test_get_token:\n"
    token = SpotifyAuth.get_access_token(user)

    sp.set_auth(token)

    user_me = sp.me()

    correct_user_me = {
        'country': 'US',
        'display_name': 'William La',
        'explicit_content': {'filter_enabled': False, 'filter_locked': False},
        'external_urls': {'spotify': 'https://open.spotify.com/user/tenzynn'},
        'followers': {'href': None, 'total': 42},
        'href': 'https://api.spotify.com/v1/users/tenzynn',
        'id': 'tenzynn',
        'images': [{'height': None, 'url': 'https://i.scdn.co/image/ab6775700000ee85b7cb260f9a5fafd5d6c15a95', 'width': None}],
        'product': 'premium',
        'type': 'user',
        'uri': 'spotify:user:tenzynn'
        }

    try:
        assert user_me == correct_user_me
        return_string += "  API call assertion passed\n"
    except AssertionError:
        return_string += "  API call assertion failed\n"

    return return_string

def test_refresh_token(user):
    return_string = "test_refresh_token:\n"

    # find user's entry in database
    db_user = db_session.query(User).filter_by(discord_id=str(user.id)).first()

    # retrieve user entry info
    old_token = db_user.access_token
    old_expires_at = db_user.expires_at
    refresh_token = db_user.refresh_token
    
    # refresh access token call
    new_token, new_expires_at = SpotifyAuth.__refresh_access_token(refresh_token)
    try: 
        assert new_expires_at != old_expires_at
        return_string += "  expires_at assertion passed\n"

    except AssertionError:
        return_string += "  expires_at assertion failed\n"

    # API call with new token
    sp.set_auth(new_token)

    user_me = sp.me()

    correct_user_me = {
        'country': 'US',
        'display_name': 'William La',
        'explicit_content': {'filter_enabled': False, 'filter_locked': False},
        'external_urls': {'spotify': 'https://open.spotify.com/user/tenzynn'},
        'followers': {'href': None, 'total': 42},
        'href': 'https://api.spotify.com/v1/users/tenzynn',
        'id': 'tenzynn',
        'images': [{'height': None, 'url': 'https://i.scdn.co/image/ab6775700000ee85b7cb260f9a5fafd5d6c15a95', 'width': None}],
        'product': 'premium',
        'type': 'user',
        'uri': 'spotify:user:tenzynn'
        }

    try:
        assert user_me == correct_user_me
        return_string += "  new_token assertion passed\n"

    except AssertionError:
        return_string += "  new_token assertion failed\n"

    # API call with old token
    sp.set_auth(old_token)
    try:
        old_user_me = sp.me()
        return_string += "  old_token call worked\n"

    except spotipy.SpotifyException:
        return_string += "  old_token call failed\n"

    return return_string

def test_spotify_id(user):
    return_string = "test_spotify_id:\n"
    result = SpotifyAuth.get_spotify_id(user)
    try:
        assert result == "tenzynn"
        return_string += "  spotify id assertion passed\n"
    except AssertionError:
        return_string += "  spotify id assertion failed\n"

    return return_string

# WHITE BOX TESTS
def test_login_permissions(user):
    pass

def test_discord_username_change(user):
    pass

async def test_all_auth(bot, user):
    test_string = ""
    # test_string += await test_login(bot, user)
    test_string += test_get_token(user)
    test_string += test_spotify_id(user)
    # test_string += test_login_permissions(user)
    # test_string += test_discord_username_change(user)
    test_string += test_refresh_token(user)
    # test_string += test_logout(user)

    test_results = open("test_results.txt", "w")
    test_results.write(test_string)
    test_results.close()