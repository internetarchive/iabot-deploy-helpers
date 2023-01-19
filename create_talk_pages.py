#!/usr/bin/python3

"""
    This script is derived from:

    MediaWiki API Demos
    Demo of `Edit` module: POST request to edit a page
    MIT license
"""

import requests
from time import sleep

lgname = ""
lgpassword = ""

def make_edit(wiki):
    S = requests.Session()

    # Step 1: GET request to fetch login token
    PARAMS_0 = {
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }

    URL = wiki + '/w/api.php'
    R = S.get(url=URL, params=PARAMS_0)
    DATA = R.json()

    LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

    # Step 2: POST request to log in. Use of main account for login is not
    # supported. Obtain credentials via Special:BotPasswords
    # (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
    PARAMS_1 = {
        "action": "login",
        "lgname": lgname,
        "lgpassword": lgpassword,
        "lgtoken": LOGIN_TOKEN,
        "format": "json"
    }

    R = S.post(URL, data=PARAMS_1)

    # Step 3: GET request to fetch CSRF token
    PARAMS_2 = {
        "action": "query",
        "meta": "tokens",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS_2)
    DATA = R.json()

    CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

    # Step 4: POST request to edit a page
    PARAMS_3 = {
        "action": "edit",
        "title": "User_talk:InternetArchiveBot",
        "token": CSRF_TOKEN,
        "format": "json",
        "text": "#REDIRECT[[meta:User talk:InternetArchiveBot]]"
    }

    R = S.post(URL, data=PARAMS_3)
    DATA = R.json()

    print(DATA)

if __name__ == '__main__':
    wikis = []

    print('Loading site matrix')
    r = requests.get('https://www.mediawiki.org/w/api.php?action=sitematrix&formatversion=2&format=json')
    r = r.json()
    r = r['sitematrix']

    for k, v in r.items():
        if type(v) is not dict:
            continue
        sites = v['site']
        for site in sites:
            if 'closed' in site:
                if site['closed'] is True:
                    continue
            if 'private' in site:
                if site['private'] is True:
                    continue
            wikis.append(site['url'])

    for wiki in wikis:
        print(wiki)
        r = requests.get(wiki + '/wiki/User_talk:InternetArchiveBot?action=raw')
        if r.status_code == 200:
            if r.text in [
                '#REDIRECT [[:w:en:User talk:InternetArchiveBot]]',
                '#REDIRECT[[:w:en:User talk:InternetArchiveBot]]',
                '#REDIRECT [[w:en:User talk:InternetArchiveBot]]',
                '#REDIRECT[[w:en:User talk:InternetArchiveBot]]',
                '#REDIRECT [[w:User talk:InternetArchiveBot]]',
                '#REDIRECT[[w:User talk:InternetArchiveBot]]',
                '#REDIRECT [[:w:User talk:InternetArchiveBot]]',
                '#REDIRECT[[:w:User talk:InternetArchiveBot]]'
            ]:
                make_edit(wiki)
                sleep(5)
            else:
                print('Skipping')
        elif r.status_code == 404:
            make_edit(wiki)
            sleep(5)
