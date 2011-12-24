import re

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
