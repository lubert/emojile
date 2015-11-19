from flask import Flask, render_template, request, jsonify
from settings import *
from auth import webauth, oauth

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

    access_token = oauth(code, redirect_uri)
    cookies = webauth(email, password, team)
    
    app.logger.info('access_token: %s' % access_token)
    app.logger.info('cookies: %s' % cookies)

    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run()
