from flask import render_template
from flask_login import current_user
import datetime

from .models.elo import elo_ref



from flask import Blueprint
bp = Blueprint('home', __name__)


@bp.route('/home')
def home():
    # get all available products for sale:
    averageElo = elo_ref.get_average(current_user.rankable_id)
    # render the page by adding information to the index.html file
    return render_template('homepage.html',
                           averageElo=averageElo)

