from flask import render_template
from flask_login import current_user
import datetime
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

    submit = SubmitField(_l('Add Activity'))

@bp.route('/activity_page', methods=['GET', 'POST'])
def activity_page():
    # get table displaying all leagues:
    a_table = Activity.get_all()

    # create a form to add a match.
    form = ActivityForm() # should i define another method for adding an activity separate from activity_page?
    if form.validate_on_submit():
        if Activity.addActivity(form.name.data):
            flash('Congratulations, you have added an Activity!')
            print('yay!')
            return redirect(url_for('activity_page.activity_page'))

    # render the page by adding information to the index.html file
    return render_template('activity_page.html',
                           activity_table=a_table, form=form)