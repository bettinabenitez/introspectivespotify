import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import SpotifyAuth.SpotifyAuth as SpotifyAuth

load_dotenv()

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

    assert user_me == correct_user_me

    return "test_get_token passed\n"

def test_refresh_token(user):
    pass

def test_spotify_id(user):
    result = SpotifyAuth.get_spotify_id(user)

    assert result == "tenzynn"

    return "test_spotify_id passed\n"

# WHITE BOX TESTS
def test_login_permissions(user):
    pass

def test_discord_username_change(user):
    pass

async def test_all_auth(bot, user):
    test_string = ""
    # test_string += await test_login(bot, user)
    # test_string += test_logout(user)
    try:
        test_string += test_get_token(user)
    except AssertionError:
        test_string += "test_get_token failed\n"
    # test_string += test_refresh_token(user)
    try:
        test_string += test_spotify_id(user)
    except AssertionError:
        test_string += "test_spotify_id failed\n"
    # test_string += test_login_permissions(user)
    # test_string += test_discord_username_change(user)
    
    test_results = open("test_results.txt", "w")
    test_results.write(test_string)
    test_results.close()