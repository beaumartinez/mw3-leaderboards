import api

if __name__ == '__main__':
    email = raw_input('Email: ')
    password = raw_input('Password: ')

    login_cookie = api.get_login_cookie(email, password)

    domination_leaderboard = api.get_domination_leaderboard(login_cookie)
    page_count, entries = api.get_domination_leaderboard_entries(domination_leaderboard)

    for entry in entries:
        print entry.to_json()
