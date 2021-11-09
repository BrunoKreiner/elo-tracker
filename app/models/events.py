from flask import current_app as app
from datetime import datetime


class Events:    
    def __init__(self, event_id, name, type,date):
        self.event_id = event_id
        self.name= name
        self.type =type
        self.date =date


# method to get every single event
    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT event_id, name, type,date
FROM Events
''')
        return [Events(*row) for row in rows]

  # method to get all past events     
    @staticmethod
    def get_all_past():
        currentDateTime = datetime.now()

        rows = app.db.execute('''
SELECT event_id, name, type,date
FROM Events
WHERE date < (:currentDateTime)
''', currentDateTime = currentDateTime)
        return [Events(*row) for row in rows]

 # method to get all past events     
    @staticmethod
    def get_all_future():
        currentDateTime = datetime.now()

        rows = app.db.execute('''
SELECT event_id, name, type,date
FROM Events
WHERE date > (:currentDateTime)
''', currentDateTime = currentDateTime)
        return [Events(*row) for row in rows]


    # method to add a new league.
    @staticmethod
    def addEvent(event_id, name, type, date): 
        rows = app.db.execute("""
INSERT INTO Events(event_id, name, type, date)
VALUES(:event_id, :name, :type, :date)
RETURNING event_id
""", event_id=event_id, name=name, type=type, date = date)
        event_id = rows[0][0] 
        return event_id




