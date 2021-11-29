from flask import render_template
from flask_login import current_user
from datetime import date
from datetime import datetime

from .models.events import Events
from.models.match import Match

from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Required
from wtforms.fields.html5 import DateField
from flask_babel import _, lazy_gettext as _l


from flask import Blueprint
bp = Blueprint('events_page', __name__)

class EventsForm(FlaskForm):
    name = StringField(_l('name'), validators=[DataRequired()])
    type = StringField(_l('type'), validators=[DataRequired()])
    date = DateField('DateTime', default = datetime.today, validators=[Required()])
    minELO = IntegerField(_l('minELO'), default = 0)
    maxELO = IntegerField(_l('maxELO'), default = 2000)
    category = SelectField('Category', choices=[('People', 'People'), ('Restaurant', 'Restaurant'), ('Code Editor', 'Code Editor'), ('School','School')], default = 'People', validators = [Required()])


    submit = SubmitField(_l('Add Event'))

## add a join events form here


@bp.route('/events_page', methods = ['GET', 'POST'])
def events_page():
    # get tables displaying events in different ways:

    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))


    events_table = Events.get_all()
    events_past_table = Events.get_all_past()
    events_future_table = Events.get_all_future()
    matches_all_table = Match.get_all()

    # create a form to add an event
    form = EventsForm()
    if form.validate_on_submit():
        now = datetime.now()
        #try:
        #    datetime.strptime(str(form.date.data), '%Y-%m-%d')
         #   print("This is the correct date string format.")
        #except ValueError:
         #   print("This is the incorrect date string format. It should be YYYY-MM-DD")


        minELOAmt = form.minELO.data
        maxELOAmt = form.maxELO.data
        if (minELOAmt >  maxELOAmt):
            flash('Failure: Your minELO needs to be less than your maxELO')
            return redirect(url_for('events_page.events_page'))
        if ((minELOAmt < 0) or (maxELOAmt < 0)):
            flash('Failure: ELO needs to be above 0')
            return redirect(url_for('events_page.events_page')) 
        if ((minELOAmt > 2000) or (maxELOAmt > 2000)):
            flash('Failure: ELO needs to be below 2000')
            return redirect(url_for('events_page.events_page'))         
        if Events.addEvent(
        form.name.data,
        form.type.data,
        form.date.data, 
        minELOAmt,
        maxELOAmt,
        form.category.data,):
            flash('Congratulations, you have added a new Event!')
            return redirect(url_for('events_page.events_page'))


    # render the page by adding information to the index.html file
    return render_template('events_page.html',
                           events_table=events_table,
                           events_past_table = events_past_table,
                           events_future_table = events_future_table,
                           form = form,
                           matches_all_table = matches_all_table)

      
@bp.route('/events_page', methods=["GET", "POST"])
def button():
    return render_template("events_page.html")
