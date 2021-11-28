from flask import render_template
from flask_login import current_user
import datetime

from .models.league import Leagues
from .models.member_of import Member_of

from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.match import Match
from .models.member_of import Member_of

from flask import Blueprint


from flask import Blueprint
bp = Blueprint('league_page', __name__)

class LeagueForm(FlaskForm):
    
    league_name = StringField(_l('League Name'), validators=[DataRequired()])
    your_name = StringField(_l('Your Name'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired()])

    submit = SubmitField(_l('Add League'))

class JoinLeagueForm(FlaskForm):

    league = StringField(_l('name'), validators=[DataRequired()])
    email = StringField(_l('email'), validators=[DataRequired()])
    status = StringField(_l('status'), validators=[DataRequired()])

    submit = SubmitField(_l('Join a League'))


@bp.route('/league_page', methods=['GET', 'POST'])
def league_page():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    
    
    form = LeagueForm()
    if form.validate_on_submit():
        # print('success')
        if Leagues.addLeague(
        form.league_name.data,
        form.your_name.data):
            if Member_of.addMember(
        form.league_name.data,
        form.email.data,
        'president'):
                print('yay!')
                return redirect(url_for('league_page.league_page'))
        
    # create a form to join a league.
    leagueform = JoinLeagueForm()
    if leagueform.validate_on_submit():
        # print('success')
        if Member_of.addMember(
        leagueform.league.data,
        leagueform.email.data,
        leagueform.status.data):
            print('yay!')
            return redirect(url_for('league_page.league_page'))
    
    
    # get table displaying all leagues:
    l_table = Leagues.get_all()

    # get table displaying user leagues: (why arent these two methods working anymore?) create.sql load
    myleagues_table = Member_of.get_user_leagues(current_user.email)

    # table of all valid statuses.
    all_statuses = Member_of.get_valid_status()

    # get table displaying leaderboard of leagues:
    leaderboard = Leagues.get_all()



    # populate the Member_of table with one more user after button push.
    # button = JoinButton() # is there a button class?
    # if button.validate_on_submit():
    #     # print('success')
    #     if Member_of.addMember(button.l_id.data,
    #     button.user_id.data,
    #     button.status.data):
    #         flash('Congratulations, you are a new league member!')
    #         print('yay!')
    #         return redirect(url_for('league_page.league_page'))



    # render the page by adding information to the index.html file
    return render_template('league_page.html',
                           league_table=l_table, myleagues_table=myleagues_table, form=form, leagueform=leagueform, all_statuses=all_statuses, leaderboard=leaderboard)


