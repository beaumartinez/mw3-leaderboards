# MW3 Leaderboards

A work-in-progress API to Modern Warfare 3's leaderboards.

## Requirements

 - [Python 2.7][python]
     - [pyquery]
     - [Requests][requests]

[pyquery]: https://bitbucket.org/olauzanne/pyquery/
[python]: http://python.org/
[requests]: http://docs.python-requests.org/en/latest/index.html

## Usage

0. [Sign up for an Elite account][elite]
1. Create an API object with your Elite account's credentials:

        api = mw3leaderboards.Api(email, password)

2. Call some methods:

        domination_leaderboard = api.get_domination_leaderboard()

        for entry in domination_leaderboard.entries:
            print entry.to_json()

[elite]: https://elite.callofduty.com/account/create
