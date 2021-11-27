from flask import render_template
from flask_login import current_user
from datetime import datetime
from .models.match import Match
from .models.elo import *
from .models.rankables import Rankables


from flask import Blueprint, redirect, url_for, request
bp = Blueprint('notifications', __name__)


@bp.route('/notifications')
def notifications():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    now = datetime.now()
    filtered_activity = None
    start_date = None
    end_date = None

    if request.method == "POST":
        print("/createlist request.method == POST")
        print(request.form)
        if request.form['activity'] != 'all':
            print(request.form['activity'])
            filtered_activity = request.form['activity']

        date_format = "%m-%d-%Y"
        try:
            datetime.strptime(request.form['start-date'], date_format)
            datetime.strptime(request.form['end-date'], date_format)
            start_date = request.form['start-date']
            end_date = request.form['end-date']
            print("This is the correct date string format.")
        except ValueError:
            print("This is the incorrect date string format. It should be MM-DD-YYYY")
        

    # get all available products for sale:
    matches = Match.get_user_history(current_user.rankable_id, filtered_activity, start_date, end_date, now)
    myActivities = Match.get_user_activities(current_user.rankable_id, now)
    print(myActivities)
    # find the products current user has bought:
    #if current_user.is_authenticated:
    #    purchases = Purchase.get_all_by_uid_since(
    #        current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    #else:
    #    purchases = None
    # render the page by adding information to the index.html file
    return render_template('notifications.html',
                            my_matches=matches, my_activities=myActivities) #,
                           #avail_products=products,
                           #purchase_history=purchases)



    # render the page by adding information to the index.html file
    return render_template('notifcations.html',rankables=r_table, elos=e_table, uninitializedIDs=uninitializedIDs)



 