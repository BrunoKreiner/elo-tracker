from flask import render_template
from flask_login import current_user
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.elo import *
from .models.rankables import Rankables
from .models.match import Match
from .models.member_of import Member_of


from flask import Blueprint, redirect, url_for, request
bp = Blueprint('players', __name__)

class ActivityForm(FlaskForm):
    activity = StringField(_l('Activity'), validators=[DataRequired()])
    submit = SubmitField(_l('Display'))

class ProfileForm(FlaskForm):
    submit = SubmitField(_l('View Profile'))


@bp.route('/players', methods=['GET', 'POST'])
def players():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    form = ActivityForm()
    formProfile= ProfileForm()

    print(form.activity.data)

    tableEntries = get_by_activity(form.activity.data)
    tableEntriesNew = []
    print(tableEntries)

    for i in range(0, len(tableEntries)):
        newEntry=[]
        newEntry.append(i+1)
        newEntry.append(Rankables.get_name(tableEntries[i][0]))
        newEntry.append(tableEntries[i][1])
        newEntry.append(tableEntries[i][0])
        tableEntriesNew.append(newEntry)

    print(tableEntriesNew)

    # render the page by adding information to the index.html file
    return render_template('players.html',formProfile=formProfile,form=form,activity=form.activity.data,tableEntries=tableEntriesNew)


@bp.route('/players/<profile_id>', methods=['POST', 'GET'])
def profile(profile_id):
    name=Rankables.get_name(profile_id)
    email=Rankables.get_email(profile_id)
    about=Rankables.get_about(profile_id)
    category=Rankables.get_category(profile_id)
    averageElo = get_average(profile_id)
    maxElo = get_max(profile_id)
    maxEloActivity = get_activity_by_elo(profile_id,maxElo)
    minElo=get_min(profile_id)
    minEloActivity=get_activity_by_elo(profile_id,minElo)
    now = datetime.now()
    numActivities = get_num_activities(profile_id)
    matchesWon = Match.get_user_num_won(profile_id, now)
    matchesPlayed = Match.get_user_num_played(profile_id, now)
    return render_template('profile.html',name=name,email=email,about=about,category=category,averageElo=averageElo, numActivities=numActivities, minElo=minElo, minEloActivity=minEloActivity, maxElo=maxElo, maxEloActivity = maxEloActivity, matchesWon = matchesWon, matchesPlayed = matchesPlayed) 
