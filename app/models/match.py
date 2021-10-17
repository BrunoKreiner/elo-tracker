from flask import current_app as app

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
        return Product(*(rows[0])) if rows is not None else None

    """
    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]"""
