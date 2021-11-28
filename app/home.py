from flask import render_template
from flask_login import current_user
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l


#from .models.elo import elo_ref
from .models.elo import *
from .models.match import Match
from .models.member_of import Member_of
from .models.rankables import Rankables



from flask import Blueprint, redirect, url_for, request
bp = Blueprint('home', __name__)

class LookupForm(FlaskForm):
    activity = StringField(_l('Activity'), validators=[DataRequired()])
    submit = SubmitField(_l('Search'))

@bp.route('/home', methods=['GET', 'POST'])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    # get all available products for sale:
    form = LookupForm()

    averageElo = get_average(current_user.rankable_id)
    maxElo = get_max(current_user.rankable_id)
    print(maxElo)
    maxEloActivity = get_activity_by_elo(current_user.rankable_id,maxElo)
    minElo=get_min(current_user.rankable_id)
    minEloActivity=get_activity_by_elo(current_user.rankable_id,minElo)
    now = datetime.now()
    numLeagues = Member_of.get_num_user_leagues(current_user.email)
    numActivities = get_num_activities(current_user.rankable_id)
    matchesWon = Match.get_user_num_won(current_user.rankable_id, now)
    matchesPlayed = Match.get_user_num_played(current_user.rankable_id, now)
    eloLookup="N/A"
    topPlayers=get_top_players("spikeball", 10)
    print(topPlayers)
    playerInfo=[]#playerInfo: (name, xyCoords)
    for player in topPlayers:
        playerInfo.append(Rankables.get_name(player[0]))
        newPoints = []
        for point in get_player_history(player[0],"spikeball"):
            newPoint = []
            newPoints.append(str(point[0]))
            newPoints.append(point[1])
        playerInfo.append(newPoints)
    
    print(playerInfo)

    if form.validate_on_submit():
        try:
            eloLookup=get_current(current_user.rankable_id, form.activity.data)
        except (exc.SQLAlchemyError, IndexError) as e:
            eloLookup="N/A"
        return render_template('homepage.html',
                           form = form, graphInfo=playerInfo, averageElo=averageElo, numActivities=numActivities, numLeagues = numLeagues, eloLookup=eloLookup, minElo=minElo, minEloActivity=minEloActivity, maxElo=maxElo, maxEloActivity = maxEloActivity, matchesWon = matchesWon, matchesPlayed = matchesPlayed)
    # render the page by adding information to the index.html file
    return render_template('homepage.html',
                           form = form, graphInfo=playerInfo, averageElo=averageElo, numActivities=numActivities, numLeagues = numLeagues, eloLookup="N/A", minElo=minElo, minEloActivity=minEloActivity, maxElo=maxElo, maxEloActivity = maxEloActivity, matchesWon = matchesWon, matchesPlayed = matchesPlayed)

