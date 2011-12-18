import api

email = raw_input('Email: ')
password = raw_input('Password: ')

api = api.Api(email, password)

domination_leaderboard = api.get_domination_leaderboard()

for entry in domination_leaderboard.entries:
    print entry.to_json()

player = raw_input('Player: ')

print api.get_player_url(player)
