from flask import current_app as app

def sortingFunc(match):
        return match[1]

class Match:
    def __init__(self, activity, id, user1_id, user2_id, user1_score, user2_score, datetime):
        self.activity = activity
        self.id = id
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.user1_score = user1_score
        self.user2_score = user2_score
        self.datetime = datetime

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
    def get_user_history(user_id):
        matches_user1 = app.db.execute('''
SELECT activity, matchID, user1_ID, user2_ID, user1_score, user2_score, date_time
FROM Matches
WHERE user1_ID = :user_id
''',
                              user_id=user_id)
        matches_user2 = app.db.execute('''
SELECT activity, matchID, user2_ID, user1_ID, user2_score, user1_score, date_time
FROM Matches
WHERE user2_ID = :user_id
''',
                              user_id=user_id)
        rows = matches_user1 + matches_user2
        rows.sort(key=sortingFunc)
        rows = [Match(*row) for row in rows]
        return rows

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
            return matchID
        except Exception as e:
            print(str(e))
            # likely email already in use; better error checking and
            # reporting needed
            return None
