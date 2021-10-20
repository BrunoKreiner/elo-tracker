from flask import render_template
from flask_login import current_user
import datetime


from .models.product import Product
from .models.purchase import Purchase



from flask import Blueprint
bp = Blueprint('league_page', __name__)


@bp.route('/league_page')
def league_page():
    # get table displaying all leagues:
    leagues = League.get_all()

    # render the page by adding information to the index.html file
    return render_template('league_page.html',
                           league_table=leagues)


# @bp.route('/home')
# def home():
#     # get all available products for sale:
#     products = Product.get_all(True)
#     # find the products current user has bought:
#     if current_user.is_authenticated:
#         purchases = Purchase.get_all_by_uid_since(
#             current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
#     else:
#         purchases = None
#     # render the page by adding information to the index.html file
#     return render_template('homepage.html',
#                            avail_products=products,
#                            purchase_history=purchases)