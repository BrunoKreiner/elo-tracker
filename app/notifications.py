from flask import render_template
from flask_login import current_user
from datetime import datetime
from .models.notifications import Notifications
from .models.elo import *


from flask import Blueprint, redirect, url_for, request
bp = Blueprint('notifications', __name__)


@bp.route('/notifications', methods = ['POST', 'GET'])
def notifications():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    now = datetime.now()
    filtered_activity = None
    start_date = None
    end_date = None
        
    notifications = Notifications.get_notifications(current_user.rankable_id)
    
    
    print('filtered activity from unconfirmed_Matchesches is: ', filtered_activity)
    return render_template('notifications.html', notifications = notifications) 
