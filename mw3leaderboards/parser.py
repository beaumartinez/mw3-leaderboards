import re

import api

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

    entry = api.DominationLeaderboardEntry(rank, name, score, time_played,
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
