from flask import render_template
from flask_login import current_user
from datetime import datetime
from .models.league import Leagues
from .models.match import Match
from .models.activity import Activity

from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from flask import Blueprint
bp = Blueprint('activity_page', __name__)


class ActivityForm(FlaskForm):

    name = StringField(_l('name'), validators=[DataRequired()])
    category = StringField(_l('category'), validators=[DataRequired()])


    submit = SubmitField(_l('Add Activity'))



@bp.route('/activity_page', methods=['GET', 'POST'])
def activity_page():
    now = datetime.now()

    # get table displaying all activities:
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    # get table displaying all leagues:
    a_table = Activity.get_all()

    # get table displaying all of my activities in previous matches I have played:
    a2_table = Match.get_user_activities(current_user.rankable_id, now)
    category = Activity.get_valid_category()
    # print(category)

    # create a form to add a league.
    form = ActivityForm() # should i define another method for adding an activity separate from activity_page?
    if form.validate_on_submit():
        # print('success')
        if Activity.addActivity(form.name.data,form.category.data):
            flash('Congratulations, you have added a new Activity!')
            return redirect(url_for('activity_page.activity_page'))
            

    # render the page by adding information to the index.html file
    return render_template('activity_page.html',
                           activity_table=a_table, my_activities_table=a2_table, form=form, category=category)