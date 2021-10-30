from flask import render_template
from flask_login import current_user
import datetime


from .models.product import Product
from .models.purchase import Purchase
from .models.match import Match


from flask import Blueprint
bp = Blueprint('history', __name__)


@bp.route('/history')
def history():
    # get all available products for sale:
    matches = Match.get_all(True)
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
