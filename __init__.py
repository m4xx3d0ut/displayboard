import redis
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from werkzeug.utils import secure_filename


db = SQLAlchemy()
sess = Session()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Flask session
    app.config['SESSION_COOKIE_NAME'] = 'session_cookie'
    app.config['SESSION_TYPE'] = os.environ.get('SESSION_TYPE')
    app.config['SESSION_REDIS'] = redis.from_url(os.environ.get('SESSION_REDIS'))

    db.init_app(app)
    sess.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Setup uploads dir
    path = os.getcwd()
    UPLOAD_FOLDER = os.path.join(path, 'uploads')

    # Check if path exists, make it if not
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)


    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    return app