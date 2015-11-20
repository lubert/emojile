from flask import Flask, render_template, request, jsonify
from settings import *
from auth import webauth, oauth
from emojis import get_emojis, post_emojis

app = Flask(__name__)
app.debug = DEBUG

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/magic', methods=['POST'])
def magic():
    email = request.form['email']
    password = request.form['password']
    team = request.form['team']
    code = request.form['code']
    redirect_uri = request.form['redirect_uri']

    team_name, access_token = oauth(code, redirect_uri)
    cookies = webauth(email, password, team)
    cookie = 'a-' + cookies['a'] + '=' + cookies['a-' + cookies['a']]
    
    app.logger.info('access_token: %s' % access_token)
    app.logger.info('team_name: %s' % team_name)
    app.logger.info('cookies: %s' % cookies)
    app.logger.info('cookie: %s' % cookie)

    get_emojis(team_name, access_token)
    post_emojis(team_name, cookie)

    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run()
