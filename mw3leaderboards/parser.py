import re

def parse_score(score):
    try:
        score = parse_formatted_number(score)
    except ValueError:
        score = re.search('(\d+\.?\d*)MM', score)
        score = score.group(1)

        score = float(score)
        score *= 1000000.0

        score = int(round(score))

    return score

def parse_formatted_number(number):
    number = number.replace(',', '')
    number = int(number)

    return number

def parse_domination_leaderboard_entry(element):
    rank_element = element[0]
    rank = rank_element.text_content()
    rank = parse_formatted_number(rank)

    name_element = element[1]
    name = name_element.text_content()
    name = name.strip()

    score_element = element[2]
    score = score_element.text_content()
    score = parse_score(score)

    captures_element = element[5]
    captures = captures_element.text_content()
    captures = parse_formatted_number(captures)

    defends_element = element[6]
    defends = defends_element.text_content()
    defends = parse_formatted_number(defends)

    kills_element = element[7]
    kills = kills_element.text_content()
    kills = parse_formatted_number(kills)

    games_played_element = element[8]
    games_played = games_played_element.text_content()
    games_played = parse_formatted_number(games_played)

    return rank, name, score, captures, defends, kills, games_played
