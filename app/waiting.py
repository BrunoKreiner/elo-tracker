from flask import render_template
from flask_login import current_user
from datetime import datetime, date
from .models.match import Match
from flask import Blueprint, redirect, url_for, request
bp = Blueprint('waiting', __name__)

@bp.route('/waiting', methods=['POST', 'GET'])
def waiting():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    now = datetime.now()

    # get all available products for sale:
    matches = Match.get_user_waiting_matches(current_user.rankable_id, now)
    
    return render_template('waiting.html', my_matches=matches) 

@bp.route('/waiting_delete/<match_id>', methods=['POST', 'GET'])
def waiting_delete(match_id):
    Match.delete(match_id)
    now = datetime.now()
    matches = Match.get_user_waiting_matches(current_user.rankable_id, now)
    
    return render_template('waiting.html', my_matches=matches) 

@bp.route('/accept/<match_id>', methods=['POST', 'GET'])
def accept(match_id):
    Match.accept(match_id)
    now = datetime.now()
    matches = Match.get_user_waiting_matches(current_user.rankable_id, now)
    
    return render_template('waiting.html', my_matches=matches) 