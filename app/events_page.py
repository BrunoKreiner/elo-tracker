from flask import render_template
from flask_login import current_user
from datetime import date
from datetime import datetime

from .models.activity import Activity
from .models.events import Events
from.models.match import Match
from .models.rankables import Rankables

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


def validate_type_category(self, name): 
        rows = Activity.get(self.type.data)
        if len(rows) < 1:
            flash('Failure: Activity is invalid')
            raise ValidationError(
                    f"Activity does not exist")
                    
def in_range(self, name): 
        minELOAmt = self.minELO.data
        maxELOAmt = self.maxELO.data
        if (minELOAmt < 0) or (maxELOAmt < 0):
            flash('Failure: ELO needs to be above 0')
            raise ValidationError(
                    f"Failure: ELO needs to be above 0")
        elif (minELOAmt > 2000) or (maxELOAmt > 2000):
            flash('Failure: ELO needs to be below 2000')
            raise ValidationError(
                    f"Failure: ELO needs to be below 2000")
        elif (minELOAmt > maxELOAmt):
            flash('Failure: Your minELO needs to be less than your maxELO')
            raise ValidationError(
                    f"Failure: Your minELO needs to be less than your maxELO")

      
    



class EventsForm(FlaskForm):
    name = StringField(_l('name'), validators=[DataRequired()])
    type = StringField(_l('type'), validators=[DataRequired(), validate_type_category])
    date = DateField('DateTime', default = datetime.today, validators=[Required()])
    minELO = IntegerField(_l('minELO'), default = 0, validators=[ in_range])
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
    

        minELOAmt = form.minELO.data
        maxELOAmt = form.maxELO.data
        myName = form.name.data
        if (len(Events.getFromName(myName))> 0):
            flash('Event Name is not Unique')
            return redirect(url_for('events_page.events_page'))  
       
        if Events.addEvent(
        myName,
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


@bp.route('/events_page/<event_id>', methods = ['GET', 'POST'])
def event_view(event_id):
     myEvent = Events.getEvent(event_id)
     myName = myEvent[1].upper()
     myType = myEvent[2].capitalize()
     myDate = myEvent[3]
     myMinElo = myEvent[4]
     myMaxElo = myEvent[5]
     myCategory = myEvent[6].capitalize()
     myMatches = Events.get_relevant_from_event(event_id)
     myMatchCount = Events.getNumberOfMatches(event_id)

     myMax1 = Events.getMax1(event_id)
     myMax2 = Events.getMax2(event_id)

     if myMax1 > myMax2:
         maxScorerUsers = Events.getMaxUser1FromEvent(event_id, myMax1)
         myMax = myMax1
     elif myMax1 < myMax2:
         maxScorerUsers = Events.getMaxUser2FromEvent(event_id, myMax2)
         myMax = myMax2
     else:
         myMax = myMax1
         myMaxUser1 = Events.getMaxUser1FromEvent(event_id, myMax1)
         myMaxUser2 = Events.getMaxUser2FromEvent(event_id, myMax2)
         maxScorerUsers = myMaxUser1.append(myMaxUser2)

    
     sizeOfList = len(maxScorerUsers)
     return render_template('event_view_page.html', 
     myName = myName,
     myType = myType,
     myDate = myDate,
     myMinElo = myMinElo,
     myMaxElo = myMaxElo,
     myCategory = myCategory,
     myMatches = myMatches,
     myMax = myMax,
     maxScorerUsers = maxScorerUsers,
     sizeOfList = sizeOfList,
     myMatchCount = myMatchCount
     )
