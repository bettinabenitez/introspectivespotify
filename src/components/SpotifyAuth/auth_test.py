import SpotifyAuth.SpotifyAuth as SpotifyAuth

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
    result = SpotifyAuth.get_spotify_id(user)

    assert result == "tenzyn"

    return "test_spotify_id pass\n"

# WHITE BOX TESTS
def test_login_permissions(user):
    pass

def test_discord_username_change(user):
    pass

async def test_all_auth(bot, user):
    test_string = ""
    # test_string += await test_login(bot, user)
    # test_string += test_logout(user)
    # test_string += test_get_token(user)
    # test_string += test_refresh_token(user)
    test_string += test_spotify_id(user)
    # test_string += test_login_permissions(user)
    # test_string += test_discord_username_change(user)
    
    test_results = open("test_results.txt", "w")
    test_results.write(test_string)
    test_results.close()