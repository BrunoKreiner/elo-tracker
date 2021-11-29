from flask import current_app as app
from datetime import datetime


class Events:    
    def __init__(self, event_id, name, type,date, minELO, maxELO, category):
        self.event_id = event_id
        self.name= name
        self.type =type
        self.date =date
        self.minELO = minELO
        self.maxELO = maxELO
        self.category = category


# method to get every single event
    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT event_id, name, type, date, minELO, maxELO,category
FROM Events
''')
        return [Events(*row) for row in rows]

  # method to get all past events     
    @staticmethod
    def get_all_past():
        currentDateTime = datetime.now()

        rows = app.db.execute('''
SELECT event_id, name, type,date, minELO, maxELO,category
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
SELECT event_id, name, type,date,minELO, maxELO,category
FROM Events
WHERE date > (:currentDateTime)
ORDER BY date, name
''', currentDateTime = currentDateTime)
        return [Events(*row) for row in rows]


    # method to add a new league.
    @staticmethod
    def addEvent(name, type, date,minELO, maxELO,category):
        if minELO is None:
            minELO = 0 
        if maxELO is None:
            maxELO = 2000
        maxEventId = app.db.execute("""
SELECT MAX(event_id)
FROM Events
        """)[0][0]

        if maxEventId is None:
            maxEventId = -1


        rows = app.db.execute("""
INSERT INTO Events(event_id, name, type, date, minELO, maxELO,category)
VALUES(:event_id, :name, :type, :date, :minELO, :maxELO, :category)
RETURNING event_id
""", 
event_id= maxEventId + 1, 
name=name, 
type=type, 
date = date, 
minELO = minELO,
 maxELO = maxELO,
 category = category)
        event_id = rows[0][0] 
        return event_id

# method to get a given whole Event by ID
    @staticmethod
    def getEvent(event_id):
        rows = app.db.execute('''
SELECT event_id,name,type,date,minELO,maxELO,category
FROM Events
WHERE event_id = (:event_id)
''', event_id = event_id)
        return rows[0]


# method to get a given event name by ID
    @staticmethod
    def getEventName(event_id):
        rows = app.db.execute('''
SELECT name
FROM Events
WHERE event_id = (:event_id)
''', event_id = event_id)
        return rows[0][0]

# method to get a given event type by ID
    @staticmethod
    def getEventType(event_id):
        rows = app.db.execute('''
SELECT type
FROM Events
WHERE event_id = (:event_id)
''', event_id = event_id)
        return rows[0][0]

# method to get a given event date by ID
    @staticmethod
    def getEventDate(event_id):
        rows = app.db.execute('''
SELECT date
FROM Events
WHERE event_id = (:event_id)
''', event_id = event_id)
        return rows[0][0]

# method to get a given event minElo by ID
    @staticmethod
    def getEventMinElo(event_id):
        rows = app.db.execute('''
SELECT minELO
FROM Events
WHERE event_id = (:event_id)
''', event_id = event_id)
        return rows[0][0]

# method to get a given event maxElo by ID
    @staticmethod
    def getEventMaxELO(event_id):
        rows = app.db.execute('''
SELECT maxELO
FROM Events
WHERE event_id = (:event_id)
''', event_id = event_id)
        return rows[0][0]

# method to get a given event category by ID
    @staticmethod
    def getEventCategory(event_id):
        rows = app.db.execute('''
SELECT category
FROM Events
WHERE event_id = (:event_id)
''', event_id = event_id)
        return rows[0][0]