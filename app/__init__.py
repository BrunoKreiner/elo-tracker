from flask import Flask
from flask_login import LoginManager
from flask_babel import Babel
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'rankables.login'
babel = Babel()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)
    babel.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .rankables import bp as user_bp
    app.register_blueprint(user_bp)

    from .home import bp as home_bp
    app.register_blueprint(home_bp)

    from .history import bp as history_bp
    app.register_blueprint(history_bp)
    from .league_page import bp as league_page_bp
    app.register_blueprint(league_page_bp)

    from .activity_page import bp as activity_page_bp
    app.register_blueprint(activity_page_bp)

    from .add_Matches import bp as add_Matches_bp
    app.register_blueprint(add_Matches_bp)

    from .events_page import bp as events_bp
    app.register_blueprint(events_bp)

    return app
