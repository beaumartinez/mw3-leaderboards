import sys

import api

try:
    email = sys.argv[1]
except IndexError:
    email = raw_input('Email: ')

try:
    password = sys.argv[2]
except IndexError:
    password = raw_input('Password: ')

api = api.Api(email, password)

for entry in api.get_domination_leaderboard():
    print entry
