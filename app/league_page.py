from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.league import Leagues


from flask import Blueprint
bp = Blueprint('league_page', __name__)


@bp.route('/league_page')
def league_page():
    # get table displaying all leagues:
    l_table = Leagues.get_all()

    # render the page by adding information to the index.html file
    return render_template('league_page.html',
                           league_table=l_table)

