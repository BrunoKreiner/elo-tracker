from flask import current_app as app
from .. import elo_calc as ec
from sqlalchemy import exc

def get_current(id, activity):

    current = app.db.execute('''
    SELECT elo
    FROM ParticipatesIn
    WHERE :id = user_ID AND :activity = activity
                            ''', id = id, activity = activity)
    return current[0][0]

#    current = app.db.execute('''
#    SELECT elo
#    FROM ELOHistory
#    WHERE :id = user_ID AND matchID in (
#        SELECT matchID, 
#        FROM Matches
#        WHERE date_time in (
#            SELECT MAX(date_time)
#            FROM Matches
#            WHERE (:id = user1_ID OR :id = user2_ID) AND :activity = activity
#        )
#    )
#                                ''', id = id, activity = activity)
    return current

def get_old(id, g_id):
    current = app.db.execute('''
    SELECT elo
    FROM ELOHistory
    WHERE matchID = :g_id AND user_ID = :id
                                ''', id = id, g_id = g_id)
    return current

def get_average(id):
    # Implementation tbd
    try:
        average = app.db.execute('''
        SELECT AVG(elo)
        FROM ParticipatesIn
        WHERE :id = user_ID
                                ''', id = id)
    except exc.SQLAlchemyError:
        average = 1000
    return average

def get_all_averages():
    averages = app.db.execute('''
    SELECT id, AVG(elo)
    FROM ParticipatesIn
    GROUP BY id
                            ''', id = id)
    return averages

# def get_all_current(id):
#     return 0

def get_max(id):
    try:
        maximum = app.db.execute('''
        SELECT MAX(elo)
        FROM ParticipatesIn
        WHERE :id = user_ID
                                ''', id = id)
    except exc.SQLAlchemyError:
        maximum = 1000
    return maximum

def get_min(id):
    try:
        minimum = app.db.execute('''
        SELECT MIN(elo)
        FROM ParticipatesIn
        WHERE :id = user_ID
                                ''', id = id)
    except exc.SQLAlchemyError:
        minimum = 1000
    return minimum

def play_game(activity, g_id, p1_id, p2_id, p1_score, p2_score):
    # Returns (p1_elo, p2_elo) from after the game is played
    print("Player one scored: {:} \nPlayer two scored: {:}".format(p1_score, p2_score))
    print("Player one id: {:} \nPlayer two id: {:}".format(p1_id, p2_id))
    p1_elo, p2_elo = ec.game(activity, p1_id, p1_score, p2_id, p2_score)
    print("Player one elo: {:} \nPlayer two elo: {:}".format(p1_elo, p2_elo))
    print("Player one id: {:} \nPlayer two id: {:}".format(p1_id, p2_id))
    p1_game = app.db.execute('''
    INSERT INTO ELOHistory(user_ID, activity, elo, matchID)
    VALUES(:p1_id, :activity, :p1_elo, :g_id)
    RETURNING elo
                                ''',
                                p1_id = p1_id,
                                activity = activity,
                                p1_elo = p1_elo,
                                g_id = g_id)
    p2_game = app.db.execute('''
    INSERT INTO ELOHistory(user_ID, activity, elo, matchID)
    VALUES(:p2_id, :activity, :p2_elo, :g_id)
    RETURNING elo
                                ''',
                                p2_id = p2_id,
                                activity = activity,
                                p2_elo = p2_elo,
                                g_id = g_id)
    p1_update = app.db.execute('''
    UPDATE ParticipatesIn
    SET elo = :p1_elo
    WHERE :p1_id = user_ID AND :activity = activity
    RETURNING elo
                                ''',
                                p1_id = p1_id,
                                activity = activity,
                                p1_elo = p1_elo)
    p2_update = app.db.execute('''
    UPDATE ParticipatesIn
    SET elo = :p2_elo
    WHERE :p2_id = user_ID AND :activity = activity
    RETURNING elo
                                ''',
                                p2_id = p2_id,
                                activity = activity,
                                p2_elo = p2_elo)
    return p1_game, p2_game

def plays_activity(activity, id):
    default_elo = 1000
    participates_in = app.db.execute('''
    INSERT INTO ParticipatesIn(user_ID, activity, elo)
    VALUES(:id, :activity, :default_elo)
    RETURNING elo
                                ''',
                                id = id,
                                activity = activity,
                                default_elo = default_elo)

def does_play(activity, id):
    does_participate = app.db.execute('''
    SELECT COUNT(1)
    FROM ParticipatesIn
    WHERE :activity = activity AND :id = user_ID
                                        ''',
                                        activity = activity,
                                        id = id)
    return does_participate == 1

def get_last_games(activity, id, n):
    games = app.db.execute('''
    SELECT user1_ID, user2_ID, user1_score, user2_score, date_time
    FROM Matches
    WHERE :activity = activity AND (:id = user1_ID OR :id = user2_ID)
    ORDER BY date_time DESC
                                ''', id = id, activity = activity)
    return games[:n]

def get_history(activity, id):
    history = app.db.execute('''
    SELECT ELOHistory.user_ID, ELOHistory.activity, ELOHistory.elo, Matches.date_time
    FROM ELOHistory LEFT OUTER JOIN Matches ON ELOHistory.matchID = Matches.matchID
    WHERE :id = ELOHistory.user_ID AND :activity = ELOHistory.activity
                                ''', id = id, activity = activity)
    return history

# Make a function that returns all the current ELOs for the activity the user plays
# Function that averages these, and maxes them