from flask import render_template, redirect, url_for, flash, request
from datetime import date
from datetime import datetime
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Required, StopValidation
from wtforms.fields.html5 import DateField
from flask_babel import _, lazy_gettext as _l

from .models.match import Match
from .models.rankables import Rankables
from .models.activity import Activity
from .models.events import Events
from .models.MatchInEvent import MatchInEvent
from .models.elo import get_current



from flask import Blueprint
bp = Blueprint('addMatches', __name__)

def validate_activity_category(self, activity):
        rows = Activity.get(self.activity.data)
        if len(rows) == 0:
            raise ValidationError(
                    f"Activity does not exist")

        user2_email = self.user2_email.data
        user2_id = Rankables.get_id_from_email(user2_email)
        user1_id = current_user.rankable_id

        if user2_id is None:
            raise StopValidation()

        user1_category = Rankables.get_category(user1_id)
        user2_category = Rankables.get_category(user2_id)
        activity_category = Activity.get_category(self.activity.data)

        if (user1_category != activity_category) or (user2_category != activity_category):
            raise ValidationError(
                    f"Users must be same category as activity")




def validate_event_category(self, event): 
    if (len(self.event.data) > 0):
        rows = Events.getFromName(self.event.data)
        if len(rows) != 1:
            raise ValidationError(
                    f"Event does not exist")
        


def validate_notself(self, user2_email):
        user2_email = self.user2_email.data
        user2_id = Rankables.get_id_from_email(user2_email)

        if user2_id is None:
            raise StopValidation(
                    f"User does not exist in system")

        user1_id = current_user.rankable_id
        if (user1_id == user2_id):
            raise ValidationError(
                    f"Cannot add a match against yourself")

class MatchForm(FlaskForm):
    user2_email = StringField(_l('Opponent\'s email'), validators=[DataRequired(), Email(), validate_notself])
    activity = StringField(_l('Activity'), validators=[DataRequired(), validate_activity_category])
    user1_score = StringField(_l('Your Score'))
    user2_score = StringField(_l('Their Score'))
    datetime = DateField('DateTime', default=datetime.today, validators=[Required()])
    event = StringField(_l('Event (optional)'), validators = [validate_event_category])
    
    submit = SubmitField(_l('Add Match'))

    


@bp.route('/addMatches', methods=['GET', 'POST'])
def addMatches():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    form = MatchForm()
    if form.validate_on_submit():
        now = datetime.now()
        try:
            datetime.strptime(str(form.datetime.data), '%Y-%m-%d')
            print("This is the correct date string format.")
        except ValueError:
            print("This is the incorrect date string format. It should be YYYY-MM-DD")

        user2_email = form.user2_email.data
        user2_id = Rankables.get_id_from_email(user2_email)
        print('other user id is', user2_id)
        user1_id = current_user.rankable_id


        form_date = datetime.strptime(str(form.datetime.data), '%Y-%m-%d')

        if (len(form.event.data)>0):
            minEloEvent = Events.getMinElo(form.event.data)
            maxEloEvent = Events.getMaxElo(form.event.data)
            try:
                user1Elo = get_current(user1_id, form.activity.data)
            except:
                user1Elo = 1000

            try:
                user2Elo = get_current(user2_id, form.activity.data)
            except:
                user2Elo = 1000

            eventType = Events.getType(form.event.data)
            eventCategory = Events.getCategory(form.event.data)
            eventDate = Events.getDate(form.event.data)
            user1Type = Rankables.get_category(user1_id)
            user2Type = Rankables.get_category(user2_id)

        issue = 0
        
        if (len(form.event.data) > 0):
            if (user1Elo < minEloEvent) or (user2Elo < minEloEvent) or (user1Elo > maxEloEvent) and (user2Elo > maxEloEvent):
                    flash('ELO of users do not qualify them to compete in this event')
                    issue = 1
            if (eventType != form.activity.data):
                    flash('This event only accepts activities of type: ' + eventType)
                    issue = 1
            if (eventCategory != user1Type ) or (eventCategory != user2Type):
                    flash('This event only accepts rankables of category: ' + eventCategory)
                    issue = 1
            if (eventDate < form.datetime.data):
                    flash('The match must be before the events enddate')
                    issue = 1
         
        if issue == 0:
            if (form_date > now):
                print('user1_score is: ', form.user1_score.data)
                print('user2_score is: ', form.user2_score.data)
                
                
                if Match.addMatch(form.activity.data,
                            current_user.rankable_id,
                            user2_id,
                            None,
                            None,
                            form.datetime.data, False):
                    flash('Congratulations, you have scheduled a future match!')
                    print('yay!')

            elif (form.user1_score.data is not None) and ((form.user2_score.data is not None)) and Match.addMatch(form.activity.data,
                            current_user.rankable_id,
                            user2_id,
                            form.user1_score.data,
                            form.user2_score.data,
                            form.datetime.data, False):
                flash('Congratulations, you have added a match!')
                print('yay!')
                #return redirect(url_for('addMatches.addMatches'))
                if (len(form.event.data) > 0):
                    matchID = Match.getMatchID()
                    MatchInEvent.addMatchAndEvent(form.event.data, matchID)
                
    return render_template('add_Matches.html', form=form)


