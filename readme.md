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

1. [Sign up for an Elite account][elite]
2. Create an API object with your Elite account's login:

        api = mw3leaderboards.Api(email, password)

3. Call some methods:

        for entry in api.get_domination_leaderboard():
            print entry

[elite]: https://elite.callofduty.com/account/create
