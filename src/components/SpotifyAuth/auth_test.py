import unittest
import SpotifyAuth.SpotifyAuth

# BLACK BOX TESTS
async def test_login(bot, user):
    pass

def test_logout(user):
    pass

def test_get_token(user):
    pass

def test_refresh_token(user):
    pass

def test_spotify_id(user):
    pass


# WHITE BOX TESTS
def test_login_permissions(user):
    pass

def test_discord_username_change(user):
    pass

async def test_all_auth(bot, user):
    await test_login(bot, user)
    test_logout(user)
    test_get_token(user)
    test_refresh_token(user)
    test_spotify_id(user)
    test_login_permissions(user)
    test_discord_username_change(user)