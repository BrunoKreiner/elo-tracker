from flask import render_template
from flask_login import current_user
import datetime

from .models.events import Events

from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l


from flask import Blueprint
bp = Blueprint('events_page', __name__)

class EventsForm(FlaskForm):
    name = StringField(_l('name'), validators=[DataRequired()])
    type = StringField(_l('type'), validators=[DataRequired()])
    date = DateTimeField(_l('date'), validators=[DataRequired()])
    minELO = IntegerField(_l('minELO'))
    maxELO = IntegerField(_l('maxELO'))

    submit = SubmitField(_l('Add Event'))

## add a join events form here


@bp.route('/events_page', methods = ['GET', 'POST'])
def events_page():
    # get tables displaying events in different ways:
    events_table = Events.get_all()
    events_past_table = Events.get_all_past()
    events_future_table = Events.get_all_future()

    # create a form to add an event
    form = EventsForm()
    if form.validate_on_submit():
        minELOAmt = form.minELO.data
        maxELOAmt = form.maxELO.data
        if (minELOAmt >  maxELOAmt):
            flash('Your minELO needs to be less than your maxELO')
            return redirect(url_for('events_page.events_page'))
        if ((minELOAmt < 0) or (maxELOAmt < 0)):
            flash('ELO needs to be above 0')
            return redirect(url_for('events_page.events_page')) 
        if ((minELOAmt > 2000) or (maxELOAmt > 2000)):
            flash('ELO needs to be below 2000')
            return redirect(url_for('events_page.events_page'))         
        if Events.addEvent(
        form.name.data,
        form.type.data,
        form.date.data, 
        minELOAmt,
        maxELOAmt):
            flash('Congratulations, you have added a new Event!')
            return redirect(url_for('events_page.events_page'))


    # render the page by adding information to the index.html file
    return render_template('events_page.html',
                           events_table=events_table,
                           events_past_table = events_past_table,
                           events_future_table = events_future_table,
                           form = form)

      
@bp.route('/events_page', methods=["GET", "POST"])
def button():
    return render_template("events_page.html")


