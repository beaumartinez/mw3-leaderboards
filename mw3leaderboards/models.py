import json

import parser

class LeaderboardEntry(object):

    def to_json(self):
        return json.dumps(self.__dict__, sort_keys=True)

    def __str__(self):
        return self.to_json()

class DominationLeaderboardEntry(LeaderboardEntry):

    def __init__(self, rank, name, score, captures, defends, kills,
            games_played):
        self.rank = rank
        self.name = name
        self.score = score
        self.captures = captures
        self.defends = defends
        self.kills = kills
        self.games_played = games_played

    @classmethod
    def from_element(cls, element):
        (rank, name, score, captures, defends, kills,
            games_played) = parser.parse_domination_leaderboard_entry(element)

        entry = cls(rank, name, score, captures, defends, kills, games_played)

        return entry

class Leaderboard(object):

    def __init__(self, entries, page_count):
        self.entries = entries
        self.page_count = page_count

    def __iter__(self):
        return iter(self.entries)
