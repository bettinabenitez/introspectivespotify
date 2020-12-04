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
    return_string = "test_login:\n"

    # testing login user not logged in
    await user.send("TESTING: Please approve the following permissions")
    message = await SpotifyAuth.spotify_login(bot, user)

    # assert that the user is successfully logged in
    try:
        assert message == "Login Successful"
        return_string += "  Login user not logged in assertion passed\n"
    except AssertionError:
        return_string += "  Login user not logged in assertion failed\n"

    # testing login user already logged in
    message = await SpotifyAuth.spotify_login(bot, user)

    # assert that the function realizes the user is already logged in
    try:
        assert message == "You've already logged in!"
        return_string += "  Login user logged in assertion passed\n"
    except AssertionError:
        return_string += "  Login user logged in assertion failed\n"

    return return_string 
        
def test_logout(user):
    return_string = "test_logout:\n"
    
    # testing logout when user is logged in
    message = SpotifyAuth.spotify_logout(user)
    
    # assert that the user is successfully logged out
    try:
        assert message == "Logout Successful"
        return_string += "  Logout user logged in assertion passed\n"
    except AssertionError:
        return_string += "  Logout user logged in assertion failed\n"

    # testing logout when user is not logged in
    message = SpotifyAuth.spotify_logout(user)

    # assert that the function realizes that the user is already logged out
    try:
        assert message == "You have not logged in!"
        return_string += "  Logout user not logged in assertion passed\n"
    except AssertionError:
        return_string += "  Logout user not logged in assertion failed\n"
    
    return return_string

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

    # assert that the Spotify API call with the access token returns the
    # expected JSON object
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

    # assert that the new expires_at time is different than the old time
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

    # assert that the Spotify API call with the new token returns the expected JSON object
    try:
        assert user_me == correct_user_me
        return_string += "  new_token assertion passed\n"

    except AssertionError:
        return_string += "  new_token assertion failed\n"

    # if the old_token is expired to begin with (as required in special setup)
    # the Spotify API call with the old token should fail
    sp.set_auth(old_token)
    try:
        old_user_me = sp.me()
        return_string += "  old_token call worked (not expected)\n"

    except spotipy.SpotifyException:
        return_string += "  old_token call failed (as expected)\n"

    return return_string

def test_spotify_id(user):
    return_string = "test_spotify_id:\n"
    result = SpotifyAuth.get_spotify_id(user)

    # assert that the spotify id returned matches the user's actual id
    try:
        assert result == "tenzynn"
        return_string += "  spotify id assertion passed\n"
    except AssertionError:
        return_string += "  spotify id assertion failed\n"

    return return_string

# WHITE BOX TESTS
async def test_login_permissions(bot, user):
    return_string = "test_login_permission:\n"

    # testing login when user denies permission
    await user.send("TESTING: please deny the permissions in the following link:")
    message = await SpotifyAuth.spotify_login(bot, user)

    # assert that the user is not logged in when they deny permissions
    try:
        assert message == "There was an error in the response I received. Please run the !login command again."
        return_string += "  Login permission assertion passed\n"
    except AssertionError:
        return_string += "  Login permission assertion failed\n"

    return return_string      

async def test_discord_username_change(bot, user):
    return_string = "test_discord_username_change:\n"

    await user.send("TESTING: please change your Discord id and reply to me once it is changed")
    await bot.wait_for('message', check=lambda m: m.author==user)

    await user.send("TESTING: logging in with a new Discord id")
    await SpotifyAuth.spotify_login(bot, user)

    # get database entries
    items = db_session.query(User).filter_by(discord_id=str(user.id))

    # assert that the number of database entries is equal to 1
    try:
        assert items.count() == 1
        return_string += "  Database entry count assertion passed\n"
    except AssertionError:
        return_string += "  Database entry count assertion failed\n"

    return return_string

async def test_all_auth(bot, user):
    # string for building test total test result output
    test_string = "Testing Results for the Spotify Authentication Component:\n\n"

    # run all the tests, record output
    test_string += await test_login_permissions(bot, user)
    test_string += await test_login(bot, user)
    test_string += await test_discord_username_change(bot, user)
    test_string += test_get_token(user)
    test_string += test_spotify_id(user)
    test_string += test_refresh_token(user)
    test_string += test_logout(user)

    # write to a test result file
    test_results = open("test_results.txt", "w")
    test_results.write(test_string)
    test_results.close()