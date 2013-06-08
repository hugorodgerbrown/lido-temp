# App models - used by SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from . import lido_app

db = SQLAlchemy(lido_app)
login_manager = LoginManager()
login_manager.init_app(lido_app)


class User(db.Model, UserMixin):
    """Basic representation of a user."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    oauth_token = db.Column(db.String(80))
    oauth_token_secret = db.Column(db.String(80))

    def __init__(self, username, token=None, secret=None):
        self.username = username
        self.oauth_token = token
        self.oauth_token_secret = secret

    def __repr__(self):
        return '<User %r>' % self.username

    def save(self):
        """Insert or update depending on whether model exists or not."""
        user = self.query.filter_by(username=self.username).first()
        if user is None:
            db.session.add(self)
        else:
            self.id = user.id
            db.session.merge(self)
        db.session.commit()

    def get_id(self):
        """Overwrite UserMixin default implementation to return username."""
        return self.username

    @classmethod
    @login_manager.user_loader
    def load_user(username):
        """Load a user from the database."""
        user = User(username=username)
        return user.query.filter_by(username=username).first()

    # @classmethod
    # @login_manager.user_loader
    # def load_user(username):
    #     user = User(username)
    #     return user.query.filter_by(username=username).first()
