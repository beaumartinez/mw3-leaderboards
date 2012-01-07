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
        rank_element = element[0]
        rank = rank_element.text_content()
        rank = parser.parse_formatted_number(rank)

        name_element = element[1]
        name = name_element.text_content()
        name = name.strip()

        score_element = element[2]
        score = score_element.text_content()
        score = parser.parse_score(score)

        captures_element = element[5]
        captures = captures_element.text_content()
        captures = parser.parse_formatted_number(captures)

        defends_element = element[6]
        defends = defends_element.text_content()
        defends = parser.parse_formatted_number(defends)

        kills_element = element[7]
        kills = kills_element.text_content()
        kills = parser.parse_formatted_number(kills)

        games_played_element = element[8]
        games_played = games_played_element.text_content()
        games_played = parser.parse_formatted_number(games_played)

        entry = cls(rank, name, score, captures, defends, kills, games_played)

        return entry

class Leaderboard(object):

    def __init__(self, entries, page_count):
        self.entries = entries
        self.page_count = page_count

    def __iter__(self):
        return iter(self.entries)
