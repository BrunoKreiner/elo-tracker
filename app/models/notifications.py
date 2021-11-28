from flask import current_app as app
from .elo import *

class Notifications:
    def __init__(self, user_id, description, datetime):
        self.user_id = user_id
        self.description = description 
        self.datetime = datetime

  

    @staticmethod
    def get_notifications(id):
        rows = app.db.execute('''
SELECT *
FROM Notifications
WHERE user_ID = :id
''',
                              id=id)
        rows = [Notifications(*row) for row in rows]
        return rows

    
   