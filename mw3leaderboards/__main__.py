import api

email = raw_input('Email: ')
password = raw_input('Password: ')

api = api.Api(email, password)

for entry in api.get_domination_leaderboard():
    print entry.to_json()
