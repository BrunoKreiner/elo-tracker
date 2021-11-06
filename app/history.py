from flask import render_template
from flask_login import current_user
from datetime import datetime


from .models.product import Product
from .models.purchase import Purchase
from .models.match import Match


from flask import Blueprint, redirect, url_for, request
bp = Blueprint('history', __name__)


@bp.route('/history', methods=['POST', 'GET'])
def history():
    now = datetime.now()

    if request.method == "POST":
        print("/createlist request.method == POST")
        print(request.form)
        filtered_activity = request.form['activity']

    # get all available products for sale:
    matches = Match.get_user_history(current_user.rankable_id, now)
    # find the products current user has bought:
    #if current_user.is_authenticated:
    #    purchases = Purchase.get_all_by_uid_since(
    #        current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    #else:
    #    purchases = None
    # render the page by adding information to the index.html file
    return render_template('history.html',
                            my_matches=matches) #,
                           #avail_products=products,
                           #purchase_history=purchases)

