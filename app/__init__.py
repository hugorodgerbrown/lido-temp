# module declaration
# this is where the Flask app itself is declared - as lido_app
import os
import flask

lido_app = flask.Flask(__name__)
lido_app.debug = True
lido_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
lido_app.secret_key = "\xdfHQ\xb5\xc6\xc9\xfb'\x1a8\x00\xab\xdcu?\x9aV\xb2$\xe8%\xa2\xdb\xf7"

# this would cause a circular import problem if it was above the
# declaration of lido_app.
import views
