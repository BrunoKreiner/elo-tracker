from flask import render_template, redirect, url_for, flash, request
from datetime import datetime
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.match import Match

from flask import Blueprint
bp = Blueprint('addMatches', __name__)

class MatchForm(FlaskForm):
    activity = StringField(_l('Activity'), validators=[DataRequired()])
    user2_id = StringField(_l('Opponent\'s User ID'), validators=[DataRequired()])
    user1_score = StringField(_l('Your Score'))
    user2_score = StringField(_l('Their Score'))
    datetime = StringField(_l('DateTime'), validators=[DataRequired()])
    
    submit = SubmitField(_l('Add Match'))


@bp.route('/addMatches', methods=['GET', 'POST'])
def addMatches():
    
    form = MatchForm()
    if form.validate_on_submit():
        now = datetime.now()
        try:
            datetime.strptime(str(form.datetime.data), '%m-%d-%Y %H:%M:%S')
            print("This is the correct date string format.")
        except ValueError:
            print("This is the incorrect date string format. It should be MM-DD-YYYY H:M:S")

        form_datetime = datetime.strptime(str(form.datetime.data), '%m-%d-%Y %H:%M:%S')
        if (form_datetime > now):
            print('user1_score is: ', form.user1_score.data)
            print('user2_score is: ', form.user2_score.data)

            if Match.addMatch(form.activity.data,
                         current_user.rankable_id,
                         form.user2_id.data,
                         None,
                         None,
                         form.datetime.data):
                flash('Congratulations, you have scheduled a future match!')
                print('yay!')

        elif Match.addMatch(form.activity.data,
                         current_user.rankable_id,
                         form.user2_id.data,
                         form.user1_score.data,
                         form.user2_score.data,
                         form.datetime.data):
            flash('Congratulations, you have added a match!')
            print('yay!')
            #return redirect(url_for('addMatches.addMatches'))
    return render_template('add_Matches.html', form=form)