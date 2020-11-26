import os
import sys
import time
import json
import spotipy
import discord
import requests
import urllib.parse as urllibparse
from urllib.parse import urlparse
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
sys.path.append('../')

# DB imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from SpotifyAuth.database_setup import Base, User

# load environment variables
load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
DB_STRING = os.getenv("DB_STRING")
CACHE_PATH = os.getenv("CACHE_PATH")

# connect to IntrospectiveSpotify database
engine = create_engine(DB_STRING)
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
db_session = Session()

# spotify variables
scope = "user-read-recently-played, user-top-read, user-read-playback-position, user-read-playback-state, user-modify-playback-state, user-read-currently-playing, playlist-modify-public, user-read-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope, cache_path=".oAuthCache"))
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
s = requests.Session()

async def spotify_login(bot, user):

    # check that user is not already logged in
    item = db_session.query(User).filter_by(discord_id=str(user.id)).first()
    if item:
        return "You've already logged in!"

    # creating login url
    # SHOULD IMPLEMENT STATE IN 2.0    
    auth_payload = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': scope,
    }
    urlparams = urllibparse.urlencode(auth_payload)
    login_url = "%s?%s" % (AUTH_URL, urlparams)

    # send url to user, get response url
    await user.send("Please log in using the following link and reply to me with the URL you are redirected to!")
    await user.send(login_url)
    await user.send("The reply URL should start with 'localhost'.")
    msg = await bot.wait_for('message', check=lambda m: m.author==user)
    auth_response = msg.content

    # parse response
    components = urlparse(auth_response)
    fragment = components.fragment
    query = components.query
    response_dict = dict(i.split('=') for i in (fragment or query or auth_response).split('&'))
    if 'error' in response_dict:
        # log error here
        await user.send("There was an error in the response I received. Please run the !login command again.")
        return "Login Failed"

    code = response_dict['code']
    
    # request to receive auth token
    token_payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    token_response = s.post(TOKEN_URL,
    data=token_payload,
    headers=headers
    )

    # handle token response
    if token_response.status_code != 200:
        # log error here
        await user.send("There was an error in the response I received. Please run the !login command again.")
        return "Login Failed"

    token_dict = token_response.json()
    token_dict['scope'] = "playlist-modify-public, user-modify-playback-state, user-read-currently-playing, user-read-playback-position, user-read-playback-state, user-read-private user-read-recently-played, user-top-read,"
    token_dict['expires_at'] = int(time.time()) + token_dict['expires_in']

    # write to oAuth cache file
    # cache_file = open(".oAuthCache", "w")
    # cache_file.write(json.dumps(token_dict))
    # cache_file.close()

    # make a call to spotify web API, verify premium
    sp.set_auth(token_dict['access_token'])
    user_me = sp.me()

    if user_me['product'] != 'premium':
        await user.send("Please upgrade to Spotify Premium if you would like to log into Introspective Spotify")
        return "Login Failed"

    # make database entry
    try:
        db_user = User(
            discord_id=str(user.id),
            spotify_name=user_me['id'],
            access_token=token_dict['access_token'],
            refresh_token=token_dict['refresh_token'],
            expires_at=token_dict['expires_at']
        )

    except SQLAlchemyError as e:
        error = type(e)
        # Log Error
        await user.send("There was an error with processing your Spotify Information. Please run !login again.")
        return "Login Failed"
    
    db_session.add(db_user)
    db_session.commit()

    return "Login Successful"


def spotify_logout(user):
    item = db_session.query(User).filter_by(discord_id=str(user.id)).first()
    if not item:
        return "You have not logged in!"

    # delete item
    db_session.delete(item)
    db_session.commit()

    return "Logout Successful"


def get_access_token(user):
    item = db_session.query(User).filter_by(discord_id=str(user.id)).first()
    if not item:
        # user is not logged in
        # methods which call get_access_token should do a None check
        return None
    
    expired = int(time.time()) - item.expires_at > 3600

    if expired:
        item.access_token, item.expires_at = __refresh_access_token(item.refresh_token)
        db_session.add(item)
        db_session.commit()

    return item.access_token


def __refresh_access_token(refresh_token):
    auth_manager = sp.auth_manager
    refresh_response = auth_manager.refresh_access_token(refresh_token)

    return (refresh_response['access_token'], refresh_response['expires_at'])


def get_spotify_id(user):
    item = db_session.query(User).filter_by(discord_id=str(user.id)).first()
    if not item:
        return "You have not logged in!"

    return item.spotify_name
