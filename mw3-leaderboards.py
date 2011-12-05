import json

import pyquery
import requests

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
        entry = _parse_domination_leaderboard_entry(entry_element)
        
        entries.append(entry)

    entries = tuple(entries)

    # Get the page count

    page_count_element = document('input[name=ajax_pagination_total]')

    page_count = page_count_element.attr('value')
    page_count = int(page_count)

    return page_count, entries

def _parse_domination_leaderboard_entry(element):
    rank_element = element[0]
    name_element = element[1]
    score_element = element[2]
    time_played_element = element[5]
    captures_element = element[6]
    defends_element = element[7]
    kills_element = element[8]
    games_played_element = element[9]

    rank = rank_element.text_content()
    name = name_element.text_content()
    score = score_element.text_content()
    time_played = time_played_element.text_content()
    captures = captures_element.text_content()
    defends = defends_element.text_content()
    kills = kills_element.text_content()
    games_played = games_played_element.text_content()

    entry = DominationLeaderboardEntry(rank, name, score, time_played,
        captures, defends, kills, games_played)

    return entry

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

if __name__ == '__main__':
    email = raw_input('Email: ')
    password = raw_input('Password: ')

    login_cookie = get_login_cookie(email, password)

    domination_leaderboard = get_domination_leaderboard(login_cookie)
    page_count, entries = get_domination_leaderboard_entries(domination_leaderboard)

    for entry in entries:
        print entry.to_json()
