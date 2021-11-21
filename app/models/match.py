from flask import current_app as app
from .elo import *

def sortingFunc(match):
        return match[1]

class Match:
    def __init__(self, activity, id, user1_id, user2_id, user1_score, user2_score, datetime, user2_name=None):
        self.activity = activity
        self.id = id
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.user2_name = user2_name
        self.user1_score = user1_score
        self.user2_score = user2_score
        self.datetime = datetime

    def to_dict(self):

        return {
            'activity': self.activity,
            'user2_name': self.user2_name,
            'user1_score': self.user1_score,
            'user2_score': self.user2_score,
            'date_time': self.datetime
        }

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT activity, matchID, user1_ID, user2_ID, user1_score, user2_score, date_time
FROM Matches
WHERE matchID = :id
''',
                              id=id)
        return Match(*(rows[0])) if rows is not None else None

    
    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT activity, matchID, user1_ID, user2_ID, user1_score, user2_score, date_time
FROM Matches
'''
                              )
        return [Match(*row) for row in rows]

    @staticmethod
    def get_all_offset(start, lim, available=True):
        rows = app.db.execute('''
SELECT activity, matchID, user1_ID, user2_ID, user1_score, user2_score, date_time
FROM Matches
LIMIT :lim
OFFSET :start
''',
                              lim=lim, start=start)
        return [Match(*row) for row in rows]

    @staticmethod
    def get_user_activities(user_id, curr_datetime):
        rows = app.db.execute('''
SELECT DISTINCT activity
FROM Matches
WHERE user1_ID = :user_id AND date_time < :curr_datetime
''',
                              user_id=user_id, curr_datetime=curr_datetime)
        return [row[0] for row in rows]

    @staticmethod
    def get_user_history_full(user_id, activity, start_time, end_time, curr_datetime):
        rows = []

        if activity is None and start_time is None:
            matches_user1 = app.db.execute('''
    SELECT activity, matchID, user1_ID, user2_ID, user1_score, user2_score, date_time
    FROM Matches
    WHERE user1_ID = :user_id AND date_time < :curr_datetime
    ''',
                                user_id=user_id, curr_datetime=curr_datetime)
            matches_user2 = app.db.execute('''
    SELECT activity, matchID, user2_ID, user1_ID, user2_score, user1_score, date_time
    FROM Matches
    WHERE user2_ID = :user_id AND date_time < :curr_datetime
    ''',
                                user_id=user_id, curr_datetime=curr_datetime)
            rows += matches_user1 + matches_user2
        elif start_time is None:
            matches_user1 = app.db.execute('''
    SELECT activity, matchID, user1_ID, user2_ID, user1_score, user2_score, date_time
    FROM Matches
    WHERE user1_ID = :user_id AND date_time < :curr_datetime AND activity = :activity
    ''',
                                user_id=user_id, curr_datetime=curr_datetime, activity=activity)
            matches_user2 = app.db.execute('''
    SELECT activity, matchID, user2_ID, user1_ID, user2_score, user1_score, date_time
    FROM Matches
    WHERE user2_ID = :user_id AND date_time < :curr_datetime AND activity = :activity
    ''',
                                user_id=user_id, curr_datetime=curr_datetime, activity=activity)
            rows += matches_user1 + matches_user2

        elif activity is None:
            matches_user1 = app.db.execute('''
    SELECT activity, matchID, user1_ID, user2_ID, user1_score, user2_score, date_time
    FROM Matches
    WHERE user1_ID = :user_id AND date_time < :curr_datetime
    AND date_time > :start_time AND date_time < :end_time
    ''',
                                user_id=user_id, curr_datetime=curr_datetime, start_time=start_time, end_time=end_time)
            matches_user2 = app.db.execute('''
    SELECT activity, matchID, user2_ID, user1_ID, user2_score, user1_score, date_time
    FROM Matches
    WHERE user2_ID = :user_id AND date_time < :curr_datetime 
    AND date_time > :start_time AND date_time < :end_time
    ''',
                                user_id=user_id, curr_datetime=curr_datetime, start_time=start_time, end_time=end_time)
            rows += matches_user1 + matches_user2
        else:
            matches_user1 = app.db.execute('''
    SELECT activity, matchID, user1_ID, user2_ID, user1_score, user2_score, date_time
    FROM Matches
    WHERE user1_ID = :user_id AND date_time < :curr_datetime
    AND date_time > :start_time AND date_time < :end_time
    AND activity = :activity
    ''',
                                user_id=user_id, curr_datetime=curr_datetime, start_time=start_time, end_time=end_time, activity=activity)
            matches_user2 = app.db.execute('''
    SELECT activity, matchID, user2_ID, user1_ID, user2_score, user1_score, date_time
    FROM Matches
    WHERE user2_ID = :user_id AND date_time < :curr_datetime 
    AND date_time > :start_time AND date_time < :end_time
    AND activity = :activity
    ''',
                                user_id=user_id, curr_datetime=curr_datetime, start_time=start_time, end_time=end_time, activity=activity)
            rows += matches_user1 + matches_user2
        #rows = matches_user1 + matches_user2
        rows.sort(key=sortingFunc)
        rows = [Match(*row) for row in rows]
        return rows

    @staticmethod
    def get_user_history(user_id, activity, start_time, end_time, curr_datetime, start_page, offset_lim, sortBy, asc):
        rows = []

        if activity is None and start_time is None:

            rows = app.db.execute('''

    SELECT T.activity, T.matchID, T.user1_ID, T.user2_ID, T.user1_score, T.user2_score, T.date_time, Rankables.name
    FROM
    
    ((SELECT activity, matchID, user1_ID, user2_ID, user1_score, user2_score, date_time
    FROM Matches
    WHERE user1_ID = :user_id AND date_time < :curr_datetime)
    UNION
    (SELECT activity, matchID, user2_ID AS user1_ID, user1_ID AS user2_ID, user2_score, user1_score, date_time
    FROM Matches
    WHERE user2_ID = :user_id AND date_time < :curr_datetime)) AS T,
    Rankables
    WHERE Rankables.rankable_id = T.user2_ID

    ORDER BY {} {}
    LIMIT :limit
    OFFSET :start_page
    '''.format(sortBy, asc),
            user_id=user_id, curr_datetime=curr_datetime, limit=offset_lim, start_page=start_page)

        elif start_time is None:

            rows = app.db.execute('''

    SELECT T.activity, T.matchID, T.user1_ID, T.user2_ID, T.user1_score, T.user2_score, T.date_time, Rankables.name
    FROM
    
    ((SELECT activity, matchID, user1_ID, user2_ID, user1_score, user2_score, date_time
    FROM Matches
    WHERE user1_ID = :user_id AND date_time < :curr_datetime AND activity = :activity)
    UNION
    (SELECT activity, matchID, user2_ID AS user1_ID, user1_ID AS user2_ID, user2_score, user1_score, date_time
    FROM Matches
    WHERE user2_ID = :user_id AND date_time < :curr_datetime AND activity = :activity)) AS T,
    Rankables
    WHERE Rankables.rankable_id = T.user2_ID

    ORDER BY {} {}
    LIMIT :limit
    OFFSET :start_page
    '''.format(sortBy, asc),
            user_id=user_id, curr_datetime=curr_datetime, activity=activity, limit=offset_lim, start_page=start_page)

        elif activity is None:

            rows = app.db.execute('''

    SELECT T.activity, T.matchID, T.user1_ID, T.user2_ID, T.user1_score, T.user2_score, T.date_time, Rankables.name
    FROM
    
    ((SELECT activity, matchID, user1_ID, user2_ID, user1_score, user2_score, date_time
    FROM Matches
    WHERE user1_ID = :user_id AND date_time < :curr_datetime
    AND date_time > :start_time AND date_time < :end_time)
    UNION
    (SELECT activity, matchID, user2_ID AS user1_ID, user1_ID AS user2_ID, user2_score, user1_score, date_time
    FROM Matches
    WHERE user2_ID = :user_id AND date_time < :curr_datetime 
    AND date_time > :start_time AND date_time < :end_time)) AS T,
    Rankables
    WHERE Rankables.rankable_id = T.user2_ID

    ORDER BY {} {}
    LIMIT :limit
    OFFSET :start_page
    '''.format(sortBy, asc),
            user_id=user_id, curr_datetime=curr_datetime, start_time=start_time, end_time=end_time, limit=offset_lim, start_page=start_page)

        else:
            rows = app.db.execute('''

    SELECT T.activity, T.matchID, T.user1_ID, T.user2_ID, T.user1_score, T.user2_score, T.date_time, Rankables.name
    FROM
    
    ((SELECT activity, matchID, user1_ID, user2_ID, user1_score, user2_score, date_time
    FROM Matches
    WHERE user1_ID = :user_id AND date_time < :curr_datetime
    AND date_time > :start_time AND date_time < :end_time
    AND activity = :activity)
    UNION
    (SELECT activity, matchID, user2_ID AS user1_ID, user1_ID AS user2_ID, user2_score, user1_score, date_time
    FROM Matches
    WHERE user2_ID = :user_id AND date_time < :curr_datetime 
    AND date_time > :start_time AND date_time < :end_time
    AND activity = :activity)) AS T,
    Rankables
    WHERE Rankables.rankable_id = T.user2_ID

    ORDER BY {} {}
    LIMIT :limit
    OFFSET :start_page
    '''.format(sortBy, asc),
            user_id=user_id, curr_datetime=curr_datetime, start_time=start_time, end_time=end_time, activity=activity, limit=offset_lim, start_page=start_page)

        rows = [Match(*row) for row in rows]
        return rows

    @staticmethod
    def get_user_num_won(user_id, curr_datetime):
        num_won_user1 = app.db.execute('''
SELECT COUNT(*)
FROM Matches
WHERE user1_ID = :user_id AND date_time < :curr_datetime AND user1_score >= user2_score
''',
                            user_id=user_id, curr_datetime=curr_datetime)
        num_won_user1 = num_won_user1[0][0]
        num_won_user2 = app.db.execute('''
SELECT COUNT(*)
FROM Matches
WHERE user2_ID = :user_id AND date_time < :curr_datetime AND user2_score >= user1_score
''',
                            user_id=user_id, curr_datetime=curr_datetime)
        num_won_user2 = num_won_user2[0][0]
        return num_won_user1 + num_won_user2

    @staticmethod
    def get_user_num_played(user_id, curr_datetime):
        
        num_played_user1 = app.db.execute('''
SELECT COUNT(*)
FROM Matches
WHERE user1_ID = :user_id AND date_time < :curr_datetime
''',
                            user_id=user_id, curr_datetime=curr_datetime)
        num_played_user1 = num_played_user1[0][0]
        num_played_user2 = app.db.execute('''
SELECT COUNT(*)
FROM Matches
WHERE user2_ID = :user_id AND date_time < :curr_datetime
''',
                            user_id=user_id, curr_datetime=curr_datetime)
        num_played_user2 = num_played_user2[0][0]
        return num_played_user1 + num_played_user2


    @staticmethod
    def addMatch(activity, user1_id, user2_id, user1_score, user2_score, datetime):

        try:
            maxMatchID = app.db.execute("""
SELECT MAX(matchID)
FROM Matches;
"""
                                  )[0][0]


            rows = app.db.execute("""
INSERT INTO Matches(activity, matchID, user1_ID, user2_ID, user1_score, user2_score, date_time)
VALUES(:activity, :matchID, :user1_id, :user2_id, :user1_score, :user2_score, :datetime)
RETURNING matchID
""",
                                  activity=activity,
                                  matchID=maxMatchID + 1,
                                  user1_id=user1_id,
                                  user2_id=user2_id,
                                  user1_score=user1_score,
                                  user2_score=user2_score,
                                  datetime=datetime)
            matchID = rows[0][0]
            if(not does_play(activity, user1_id)):
                plays_activity(activity, user1_id)
            if(not does_play(activity, user2_id)):
                plays_activity(activity, user2_id)
            play_game(activity, matchID, user1_id, user2_id, user1_score, user2_score)
            print(app.db.execute('''
            SELECT user_ID, activity, elo
            FROM ParticipatesIn
                                '''))
            return matchID
        except Exception as e:
            print(str(e))
            # likely email already in use; better error checking and
            # reporting needed
            return None
