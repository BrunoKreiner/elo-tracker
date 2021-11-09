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
ORDER BY date DESC, name

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
ORDER BY date, name
''', currentDateTime = currentDateTime)
        return [Events(*row) for row in rows]


    # method to add a new league.
    @staticmethod
    def addEvent(name, type, date): 
        maxEventId = app.db.execute("""
SELECT MAX(event_id)
FROM Events
        """)[0][0]
        rows = app.db.execute("""
INSERT INTO Events(event_id, name, type, date)
VALUES(:event_id, :name, :type, :date)
RETURNING event_id
""", event_id= maxEventId +1, name=name, type=type, date = date)
        event_id = rows[0][0] 
        return event_id




