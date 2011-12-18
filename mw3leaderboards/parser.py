import re

import api

def _parse_domination_leaderboard_entry(element):
    rank_element = element[0]
    name_element = element[1]
    score_element = element[2]
    captures_element = element[5]
    defends_element = element[6]
    kills_element = element[7]
    games_played_element = element[8]

    rank = rank_element.text_content()
    name = name_element.text_content()
    score = score_element.text_content()
    captures = captures_element.text_content()
    defends = defends_element.text_content()
    kills = kills_element.text_content()
    games_played = games_played_element.text_content()

    rank = rank.replace(',', '')
    rank = int(rank)

    score = _parse_score(score)

    captures = captures.replace(',', '')
    captures = int(captures)

    defends = defends.replace(',', '')
    defends = int(defends)

    kills = kills.replace(',', '')
    kills = int(kills)

    games_played = games_played.replace(',', '')
    games_played = int(games_played)

    entry = api.DominationLeaderboardEntry(rank, name, score, captures, defends,
        kills, games_played)

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
