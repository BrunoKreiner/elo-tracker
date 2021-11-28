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

    from .unconfirmed_Matches import bp as unconfirmedMatches_bp
    app.register_blueprint(unconfirmedMatches_bp)

    from .pending import bp as pending_bp
    app.register_blueprint(pending_bp)

    from .waiting import bp as waiting_bp
    app.register_blueprint(waiting_bp)

    from .futureMatches import bp as futureMatches_bp
    app.register_blueprint(futureMatches_bp)

    from .league_page import bp as league_page_bp
    app.register_blueprint(league_page_bp)

    from .activity_page import bp as activity_page_bp
    app.register_blueprint(activity_page_bp)

    from .add_Matches import bp as add_Matches_bp
    app.register_blueprint(add_Matches_bp)
    
    from .players import bp as players_bp
    app.register_blueprint(players_bp)

    from .events_page import bp as events_bp
    app.register_blueprint(events_bp)
    
    from .notifications import bp as notifications_bp
    app.register_blueprint(notifications_bp)

    return app
