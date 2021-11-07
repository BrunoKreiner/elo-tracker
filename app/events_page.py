from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.league import Leagues


from flask import Blueprint
bp = Blueprint('events_page', __name__)


@bp.route('/events_page')
def events_page():
    # get table displaying all leagues:
    events_table = Events.get_all()

    # render the page by adding information to the index.html file
    return render_template('events_page.html',
                           events_table=events_table)

