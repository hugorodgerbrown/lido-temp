# app views
from flask import (
    # Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash
)
import flask_login
from . import lido_app
from auth import twitter
from models import User


@lido_app.route('/')
def index():
    return render_template(
        'chart.html',
        browser=request.user_agent.browser
    )


    @lido_app.route('/login')
    def login():
        return twitter.authorize(
            callback=url_for(
                'oauth_authorized',
                next=request.args.get('next') or request.referrer or None)
        )

    @twitter.tokengetter
    def get_twitter_token(token=None):
        return session.get('twitter_token')

    @lido_app.route('/oauth-authorized')
    @twitter.authorized_handler
    def oauth_authorized(resp):
        print 'foo-bar'
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    user = User.get_user(resp['screen_name'])
    if user is None:
        user = User(
            username=resp['screen_name'],
            token=resp['oauth_token'],
            secret=resp['oauth_token_secret']
        )
    else:
        user.oauth_token = resp['oauth_token']
        user.oauth_token_secret = resp['oauth_token_secret']
    user.save()

    # use flask_login to set up the user session stuff
    flask_login.login_user(user)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)
