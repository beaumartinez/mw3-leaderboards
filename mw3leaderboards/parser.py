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
