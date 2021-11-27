from flask import render_template
from flask_login import current_user
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.elo import *
from .models.rankables import Rankables


from flask import Blueprint, redirect, url_for, request
bp = Blueprint('players', __name__)

class ActivityForm(FlaskForm):
    activity = StringField(_l('Activity'), validators=[DataRequired()])
    submit = SubmitField(_l('Confirm'))


@bp.route('/players')
def players():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    form = ActivityForm()
    
    r_table = Rankables.get_all_visible()
    e_table = get_all_averages()
    uninitializedIDs = []

    for player in r_table:
        hit = 0
        for row in e_table:
            if row[0] == player.rankable_id:
                hit = 1
        if not hit:
            uninitializedIDs.append(player.rankable_id)

    # render the page by adding information to the index.html file
    return render_template('players.html',rankables=r_table, elos=e_table, uninitializedIDs=uninitializedIDs)