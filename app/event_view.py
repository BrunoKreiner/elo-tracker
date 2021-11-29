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
    #  myMatches = Match.get_all_in_event(event_id)    


from flask import Blueprint
bp = Blueprint('events_page', __name__)

@bp.route('/events_page/<event_id>', methods = ['POST', 'GET'])
def event(event_id):
     return render_template('event_view_page.html')#, my_matches=myMatches) 
