from flask import render_template
from flask_login import current_user
import datetime

from .models.elo import elo_ref
from .models.match import Match



from flask import Blueprint, redirect, url_for, request
bp = Blueprint('home', __name__)


@bp.route('/home', methods=['GET', 'POST'])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    # get all available products for sale:
    averageElo = elo_ref.get_average(current_user.rankable_id)
    maxElo = elo_ref.get_max(current_user.rankable_id)
    matchesWon = Match.get_user_num_won(current_user.rankable_id)
    matchesPlayed = Match.get_user_num_played(current_user.rankable_id)
    # render the page by adding information to the index.html file
    return render_template('homepage.html',
                           averageElo=averageElo, maxElo=maxElo, matchesWon = matchesWon, matchesPlayed = matchesPlayed)

