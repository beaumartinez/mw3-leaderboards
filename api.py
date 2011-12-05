import json

import pyquery
import requests

import parser

def get_login_cookie(email, password):
    credentials = {
        'j_username': email,
        'j_password': password,
    }

    request = requests.post('https://profile.callofduty.com/p/process_login',
        data=credentials)

    return request.cookies

def get_domination_leaderboard(login_cookie, page=1):
    request = requests.get('https://elite.callofduty.com/leaderboards/mw3/regular/domination/alltime?page={}'.format(page), cookies=login_cookie)

    return request.content

def get_domination_leaderboard_entries(domination_leaderboard):
    '''Return a tuple (page_count, entries).'''
    entries = list()

    document = pyquery.PyQuery(domination_leaderboard)

    # Get the leaderboard entries

    table_rows = document('#beachhead tr')

    # The first row is the header row
    entry_elements = table_rows[1:]

    for entry_element in entry_elements:
        entry = parser._parse_domination_leaderboard_entry(entry_element)
        
        entries.append(entry)

    entries = tuple(entries)

    # Get the page count

    page_count_element = document('input[name=ajax_pagination_total]')

    page_count = page_count_element.attr('value')
    page_count = int(page_count)

    return page_count, entries

class DominationLeaderboardEntry(object):

    def __init__(self, rank, name, score, time_played, captures, defends, kills,
            games_played):
        self.rank = rank
        self.name = name
        self.score = score
        self.time_played = time_played
        self.captures = captures
        self.defends = defends
        self.kills = kills
        self.games_played = games_played

    def to_json(self):
        return json.dumps(self.__dict__)
