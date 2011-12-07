import json

import pyquery
import requests

import parser

class Api(object):

    def __init__(self, email, password):
        self.email = email
        self.password = password

        self._log_in()

    def _log_in(self):
        credentials = {
            'j_username': self.email,
            'j_password': self.password,
        }

        request = requests.post(
            'https://profile.callofduty.com/p/process_login', data=credentials)

        self._login_cookie = request.cookies

    def get_domination_leaderboard(self, page=1):
        request = requests.get('https://elite.callofduty.com/leaderboards/mw3/'
            'regular/domination/alltime?page={}'.format(page),
            cookies=self._login_cookie)

        document = pyquery.PyQuery(request.content)

        # Get the leaderboard entries

        entries = list()

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

        leaderboard = Leaderboard(entries, page_count)

        return leaderboard

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

class Leaderboard(object):

    def __init__(self, entries, page_count):
        self.entries = entries
        self.page_count = page_count
