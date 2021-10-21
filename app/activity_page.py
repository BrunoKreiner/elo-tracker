from flask import render_template
from flask_login import current_user
import datetime


from .models.product import Product
from .models.purchase import Purchase
from .models.league import Leagues
from .models.activity import Activity


from flask import Blueprint
bp = Blueprint('activity_page', __name__)


@bp.route('/activity_page')
def league_page():
    # get table displaying all leagues:
    a_table = Activity.get_all()

    # render the page by adding information to the index.html file
    return render_template('activity_page.html',
                           activity_table=a_table)