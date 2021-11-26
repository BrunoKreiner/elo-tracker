from flask import render_template
from flask_login import current_user
from datetime import datetime


from .models.elo import elo_ref
from .models.elo import *
from .models.match import Match



from flask import Blueprint, redirect, url_for, request
bp = Blueprint('home', __name__)


@bp.route('/home', methods=['GET', 'POST'])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    # get all available products for sale:
    averageElo = get_average(current_user.rankable_id)
    maxElo = get_max(current_user.rankable_id)
    now = datetime.now()
    matchesWon = Match.get_user_num_won(current_user.rankable_id, now)
    matchesPlayed = Match.get_user_num_played(current_user.rankable_id, now)
    # render the page by adding information to the index.html file
    return render_template('homepage.html',
                           averageElo=averageElo, maxElo=maxElo, matchesWon = matchesWon, matchesPlayed = matchesPlayed)

