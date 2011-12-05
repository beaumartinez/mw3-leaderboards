import json
import re

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

    rank = rank.replace(',', '')
    rank = int(rank)

    score = _parse_score(score)

    captures = captures.replace(',', '')
    captures = int(captures)

    time_played = _parse_time(time_played)

    defends = defends.replace(',', '')
    defends = int(defends)

    kills = kills.replace(',', '')
    kills = int(kills)

    games_played = games_played.replace(',', '')
    games_played = int(games_played)

    entry = DominationLeaderboardEntry(rank, name, score, time_played,
        captures, defends, kills, games_played)

    return entry

def _parse_score(score):
    score = score.replace(',', '')

    try:
        score = int(score)
    except ValueError:
        score = re.search('(\d+\.?\d*)MM', score)
        score = score.group(1)

        score = float(score)
        score *= 1000000

        score = int(score)

    return score

def _parse_time(time):
    weeks = re.search('(\d+)w', time)
    days = re.search('(\d+)d', time)
    hours = re.search('(\d+)h', time)
    minutes = re.search('(\d+)m', time)
    seconds = re.search('(\d+)s', time)

    try:
        weeks = weeks.group(1)
    except AttributeError:
        weeks = 0
    else:
        weeks = int(weeks)

    try:
        days = days.group(1)
    except AttributeError:
        days = 0
    else:
        days = int(days)

    try:
        hours = hours.group(1)
    except AttributeError:
        hours = 0
    else:
        hours = int(hours)

    try:
        minutes = minutes.group(1)
    except AttributeError:
        minutes = 0
    else:
        minutes = int(minutes)

    try:
        seconds = seconds.group(1)
    except AttributeError:
        seconds = 0
    else:
        seconds = int(seconds)

    seconds += (minutes * 60)
    seconds += (hours * 360)
    seconds += (days * 8640)
    seconds += (weeks * 60480)

    return seconds

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
