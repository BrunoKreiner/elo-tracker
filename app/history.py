from flask import render_template
from flask_login import current_user
from datetime import datetime, date

from .models.match import Match


from flask import Blueprint, redirect, url_for, request
bp = Blueprint('history', __name__)

@bp.route('/data', methods=['POST', 'GET'])
def data():

    start_date = None
    end_date = None
    filtered_activity = None

    if request.method == "POST":
        print("YASS")
        print(request.form)

    if request.method == "POST":
        if request.form['filterActivity'] != 'None':
            print('filtered_activity is: ', request.form['filterActivity'])
            filtered_activity = request.form['filterActivity']

        date_format = "%Y-%m-%d"
        try:
            datetime.strptime(request.form['startDate'], date_format)
            datetime.strptime(request.form['endDate'], date_format)
            start_date = request.form['startDate']
            end_date = request.form['endDate']
            print("This is the correct date string format.")
        except ValueError:
            print("This is the incorrect date string format. It should be MM-DD-YYYY")

    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))

    now = datetime.now()
    
    query = Match.get_user_history_full(current_user.rankable_id, None, None, None, now)
    total_unfiltered = len(query)

    query = Match.get_user_history_full(current_user.rankable_id, filtered_activity, start_date, end_date, now)
    total_filtered = len(query)
    print('total_filtered is :', total_filtered)

    # pagination 
    start = request.form['start']
    length = request.form['length']

    # sorting
    col_index = request.form['order[0][column]']
    col_name = request.form[f'columns[{col_index}][data]']
    if col_name == None:
        col_name = 'date_time'

    asc = 'ASC'
    if request.form[f'order[0][dir]'] == 'desc':
        asc = 'DESC'

    query = Match.get_user_history(current_user.rankable_id, filtered_activity, start_date, end_date, now, start, length, col_name, asc)
    print('queries done')

    # response
    return {
        'data': [user.to_dict() for user in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': total_unfiltered,
        'draw': int(request.form['draw']),
    }


@bp.route('/history', methods=['POST', 'GET'])
def history():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    now = datetime.now()
    filtered_activity = None
    start_date = None
    end_date = None

    if request.method == "POST":
        print("/createlist request.method == POST")
        #print(request.form)
        if request.form['activity'] != 'all':
            print(request.form['activity'])
            filtered_activity = request.form['activity']

        date_format = "%Y-%m-%d"
        try:
            datetime.strptime(request.form['start-date'], date_format)
            datetime.strptime(request.form['end-date'], date_format)
            start_date = request.form['start-date']
            start_time = start_date
            end_date = request.form['end-date']
            end_time = end_date
            print("This is the correct date string format.")
        except ValueError:
            print("This is the incorrect date string format. It should be MM-DD-YYYY")
            print('yeah so the format is currently', request.form['start-date'])
        

    # get all available products for sale:
    #matches = Match.get_user_history(current_user.rankable_id, filtered_activity, start_date, end_date, now)
    myActivities = Match.get_user_activities(current_user.rankable_id, now)
    # find the products current user has bought:
    #if current_user.is_authenticated:
    #    purchases = Purchase.get_all_by_uid_since(
    #        current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    #else:
    #    purchases = None
    # render the page by adding information to the index.html file
    print('filtered activity from history is: ', filtered_activity)
    return render_template('history.html', my_activities=myActivities, filterActivity=filtered_activity,
                                            start_date=start_date, end_date=end_date) 

