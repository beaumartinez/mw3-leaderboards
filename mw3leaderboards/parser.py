import re

import models

def _parse_domination_leaderboard_entry(element):
    rank_element = element[0]
    rank = rank_element.text_content()
    rank = rank.replace(',', '')
    rank = int(rank)

    name_element = element[1]
    name = name_element.text_content()
    name = name.strip()

    score_element = element[2]
    score = score_element.text_content()
    score = _parse_score(score)

    captures_element = element[5]
    captures = captures_element.text_content()
    captures = captures.replace(',', '')
    captures = int(captures)

    defends_element = element[6]
    defends = defends_element.text_content()
    defends = defends.replace(',', '')
    defends = int(defends)

    kills_element = element[7]
    kills = kills_element.text_content()
    kills = kills.replace(',', '')
    kills = int(kills)

    games_played_element = element[8]
    games_played = games_played_element.text_content()
    games_played = games_played.replace(',', '')
    games_played = int(games_played)

    entry = models.DominationLeaderboardEntry(rank, name, score, captures,
        defends, kills, games_played)

    return entry

def _parse_score(score):
    score = score.replace(',', '')

    try:
        score = int(score)
    except ValueError:
        score = re.search('(\d+\.?\d*)MM', score)
        score = score.group(1)

        score = float(score)
        score *= 1000000.0

        score = int(round(score))

    return score
