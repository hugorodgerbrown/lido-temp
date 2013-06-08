# App models - used by SQLAlchemy
import datetime
from flask_login import UserMixin, LoginManager
from . import lido_app, db

login_manager = LoginManager()
login_manager.init_app(lido_app)


class User(db.Model, UserMixin):
    """Basic representation of a user."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    oauth_token = db.Column(db.String(80))
    oauth_token_secret = db.Column(db.String(80))
    recordings = db.relationship('TemperatureRecord')

    def __init__(self, username, token=None, secret=None):
        self.username = username
        self.oauth_token = token
        self.oauth_token_secret = secret

    def __repr__(self):
        return '<User: %r>' % self.username

    def save(self):
        """Save User record. Raises IntegrityError if duplicate."""
        db.session.add(self)
        db.session.commit()

    def get_id(self):
        """Overwrite UserMixin default implementation to return username."""
        return self.username

    def submit_temperature_recording(location, temperature):
        """Save a new temp. recording."""
        pass

    @classmethod
    @login_manager.user_loader
    def get_user(username):
        """Load a user from the database."""
        return User.query.filter_by(username=username).first()


class TemperatureRecord(db.Model):
    """An individual temp recording, submitted by a User, for a lido."""

    id = db.Column(db.Integer, primary_key=True)
    submitted_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    submitted_by = db.relationship('User')
    submitted_at = db.Column(db.DateTime(timezone=True))
    location = db.Column(db.String(50))
    temperature = db.Column(db.Float)

    def __init__(self, user, location, temperature, timestamp=None):
        self.submitted_by_id = user.id
        self.location = location
        self.temperature = temperature
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return '<Temperature: %s @ %s>' % (self.temperature, self.location)

    def save(self):
        """Insert or update depending on whether model exists or not."""
        db.session.add(self)
        db.session.commit()
