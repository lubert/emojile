import json, requests, urllib
from settings import *
from bs4 import BeautifulSoup
from flask import jsonify

def oauth(code, redirect_uri):
    """Returns access token given an exchange code

    See https://api.slack.com/docs/oauth
    """
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': redirect_uri
    }

    res = requests.get('https://slack.com/api/oauth.access', params=payload)
    data = json.loads(res.content)

    if not data['ok']:
        return

    return (data['team_name'], data['access_token'])

def webauth(email, password, team):
    """Returns cookies through web authentication

    Grabs CSRF token and posts login credentials to the team endpoint
    """
    url = 'https://%s.slack.com' % team
    s = requests.Session()
    s.headers.update({
        'Pragma': 'no-cache',
        'Origin': 'null',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8,de;q=0.6',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.49 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
    })

    # get csrf token
    res = s.get(url)
    crumb = get_crumb(res.content)

    # get login cookie
    data = 'signin=1&crumb={0}&email={1}&password={2}'.format(crumb, email, password)
    res = s.post('https://%s.slack.com/' % team, data=data, allow_redirects=False)

    if 'a' not in res.cookies:
        return

    return res.cookies.get_dict()

def get_crumb(html):
    soup = BeautifulSoup(html, 'html.parser')
    val = soup.find('input',{'name': 'crumb'})['value']
    crumb = urllib.quote(val.encode('utf8'), safe='~@#$&()*!+=:;,.?/\'')
    return crumb
