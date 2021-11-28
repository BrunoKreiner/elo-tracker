from flask import render_template
from flask_login import current_user
from datetime import datetime, date
from .models.match import Match
from flask import Blueprint, redirect, url_for, request
bp = Blueprint('pending', __name__)

@bp.route('/pending', methods=['POST', 'GET'])
def pending():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    now = datetime.now()

    # get all available products for sale:
    matches = Match.get_user_pending_matches(current_user.rankable_id, now)

    return render_template('pending.html', my_matches=matches) 



