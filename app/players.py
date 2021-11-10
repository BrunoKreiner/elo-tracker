from flask import render_template
from flask_login import current_user
import datetime


from .models.product import Product
from .models.purchase import Purchase
from .models.rankables import Rankables


from flask import Blueprint, redirect, url_for, request
bp = Blueprint('players', __name__)


@bp.route('/players')
def players():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    r_table = Rankables.get_all_visible()

    # render the page by adding information to the index.html file
    return render_template('players.html',rankables=r_table)