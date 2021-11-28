from flask import render_template
from flask_login import current_user
from datetime import datetime, date
from .models.match import Match
from flask import Blueprint, redirect, url_for, request
bp = Blueprint('futureMatches', __name__)

@bp.route('/futureMatches', methods=['POST', 'GET'])
def futureMatches():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    now = datetime.now()
    matches = Match.get_user_future_matches(current_user.rankable_id, now)
    return render_template('futureMatches.html', my_matches=matches) 

@bp.route('/delete_future/<match_id>', methods=['POST', 'GET'])
def delete_future(match_id):
    Match.delete(match_id)
    now = datetime.now()
    matches = Match.get_user_future_matches(current_user.rankable_id, now) 
    return render_template('futureMatches.html', my_matches=matches) 
