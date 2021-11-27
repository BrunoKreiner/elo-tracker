from flask import render_template
from flask_login import current_user
from datetime import datetime, date
from .models.match import Match
from flask import Blueprint, redirect, url_for, request
bp = Blueprint('unconfirmedMatches', __name__)

@bp.route('/unconfirmedMatches', methods=['POST', 'GET'])
def unconfirmedMatches():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    now = datetime.now()
    filtered_activity = None
    start_date = None
    end_date = None
        

    # get all available products for sale:
    matches = Match.get_user_incomplete_matches(current_user.rankable_id, filtered_activity, start_date, end_date, now, 0, 100000, 'date_time', 'ASC')
    myActivities = Match.get_user_activities(current_user.rankable_id, now)
    # find the products current user has bought:
    #if current_user.is_authenticated:
    #    purchases = Purchase.get_all_by_uid_since(
    #        current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    #else:
    #    purchases = None
    # render the page by adding information to the index.html file
    print('filtered activity from unconfirmed_Matchesches is: ', filtered_activity)
    return render_template('unconfirmedMatches.html', my_matches=matches, my_activities=myActivities, filterActivity=filtered_activity,
                                            start_date=start_date, end_date=end_date) 

@bp.route('/forward/<match_id>', methods=['POST', 'GET'])
def forward(match_id):
    print('forward match id is: ', match_id)

    Match.delete(match_id)
    now = datetime.now()
    matches = Match.get_user_incomplete_matches(current_user.rankable_id, None, None, None, now, 0, 100000, 'date_time', 'ASC')
    
    return render_template('unconfirmedMatches.html', my_matches=matches) 

@bp.route('/edit/<match_id>', methods=['POST', 'GET'])
def edit(match_id):
    print('edit match id is: ', match_id)

    myScore = request.form['my-score']
    theirScore = request.form['their-score']

    match = Match.get(match_id)
    user1_id = match.user1_id
    user2_id = match.user2_id
    user1_score = myScore
    user2_score = theirScore
    if (match.user2_id == current_user.rankable_id):
    # need to switch them in the table
        user1_id = match.user2_id
        user2_id = match.user1_id
        user1_score = theirScore
        user2_score = myScore

    Match.editScore(match_id, user1_id, user2_id, user1_score, user2_score)

    if request.method == "POST":
        print('edit form is', request.form)
    
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    now = datetime.now()

    # get all available products for sale:
    matches = Match.get_user_incomplete_matches(current_user.rankable_id, None, None, None, now, 0, 100000, 'date_time', 'ASC')
    
    return render_template('unconfirmedMatches.html', my_matches=matches) 