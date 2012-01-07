import urlparse

import pyquery
import requests

import models

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

        request = requests.post('https://profile.callofduty.com/p/'
            'process_login', data=credentials)

        self._login_cookie = request.cookies

    def get_domination_leaderboard(self, page=1):
        request = requests.get('https://elite.callofduty.com/leaderboards/mw3/'
            'regular/domination/alltime?page={}'.format(page),
            cookies=self._login_cookie)

        # TODO: Abstract this kind of parsing

        document = pyquery.PyQuery(request.content)

        # Get the leaderboard entries

        entries = list()

        table_rows = document('#beachhead tr')

        # The first row is the header row
        entry_elements = table_rows[1:]

        for entry_element in entry_elements:
            entry = models.DominationLeaderboardEntry.from_element(
                entry_element)
            
            entries.append(entry)

        entries = tuple(entries)

        # Get the page count

        page_count_element = document('input[name=ajax_pagination_total]')

        page_count = page_count_element.attr('value')
        page_count = int(page_count)

        leaderboard = models.Leaderboard(entries, page_count)

        return leaderboard

    def get_player_url(self, player):
        SEARCH_URL = 'https://elite.callofduty.com/search'

        arguments = {
            'name': player,
        }

        request = requests.post(SEARCH_URL, data=arguments,
            cookies=self._login_cookie, allow_redirects=True)

        player_url = request.url

        # Elite redirects to the search URL if there isn't a match
        if player_url == SEARCH_URL:
            player_url = None

        # Get the player_id

        try:
            split_player_url = urlparse.urlsplit(player_url)
        except AttributeError:
            player_id = None
        else:
            path = split_player_url.path
            path = path.split('/')

            # Remove the first "/"  
            path = path[1:]

            player_id = path[1:]
            player_id = '/'.join(player_id)

        return player_id, player_url
