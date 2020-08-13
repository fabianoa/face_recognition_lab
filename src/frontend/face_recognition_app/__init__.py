# app/__init__.py

# third-party imports
from flask import abort, Flask, render_template
from flask_login import LoginManager

from flask_bootstrap import Bootstrap

# local imports
from face_recognition_app.config import app_config
import os

config_name = os.getenv('FLASK_CONFIG')

# login manager initialisation
login_manager = LoginManager()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config[config_name])
#app.config.from_pyfile('config.py')

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key",
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']),
    UPLOAD_FOLDER='/static/img/uploads'
    ))
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


Bootstrap(app)  # seems to be required for routes with prefixes to work...
login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.login"

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .home import home as home_blueprint
app.register_blueprint(home_blueprint)

from .face_recogntion import  face_recognition as face_regonition_blueprint
app.register_blueprint(face_regonition_blueprint, url_prefix='/face_regonition')
    
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html', title='Forbidden'), 403

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', title='Page Not Found'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', title='Server Error'), 500
