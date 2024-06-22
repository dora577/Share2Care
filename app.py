from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()

    # Get configuration from environment variables
    SECRET_KEY = os.getenv('SECRET_KEY')
    PASSWORD = os.getenv('PASSWORD')
    PUBLIC_IP_ADDRESS = os.getenv('PUBLIC_IP_ADDRESS')
    DBNAME = os.getenv('DBNAME')
    PROJECT_ID = os.getenv('PROJECT_ID')
    INSTANCE_NAME = os.getenv('INSTANCE_NAME')

    # Configuration
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}"
        f"?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from models import Users

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    # Blueprint for auth routes in our app
    from authorization import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
