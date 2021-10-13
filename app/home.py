from flask import render_template
from flask_login import current_user
import datetime



from flask import Blueprint
bp = Blueprint('home', __name__)


@bp.route('/home')
def home():

    return render_template('homepage.html')
