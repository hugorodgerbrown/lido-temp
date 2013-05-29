"""
stats.py web app used to generate data for geckoboard.
"""
from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash
)
from flask_oauth import OAuth
from os import environ as env

app = Flask(__name__)
app.debug = True

CONSUMER_KEY = env['CONSUMER_KEY']
CONSUMER_SECRET = env['CONSUMER_SECRET']

oauth = OAuth()
twitter = oauth.remote_app(
    'twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET
)


@app.route('/')
def temp():
    return render_template('chart.html', browser=request.user_agent.browser)


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@app.route('/login')
def login():
    return twitter.authorize(callback=url_for(
        'oauth_authorized',
        next=request.args.get('next') or request.referrer or None)
    )


@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)


app.secret_key = 'asdfa ewrt4534qfg reqg afd '

if __name__ == '__main__':
    app.run()
