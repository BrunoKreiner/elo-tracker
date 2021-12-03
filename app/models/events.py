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
SELECT event_id,name,type,to_char(date,'Month DD, YYYY'),minELO,maxELO,category
FROM Events
WHERE event_id = (:event_id)
''', event_id = event_id)
        return rows[0]

# method to get a given category by name
    @staticmethod
    def getCategory(event_name):
        rows = app.db.execute('''
SELECT category
FROM Events
WHERE name = (:event_name)
''', event_name = event_name)
        return rows[0][0]


# method to get a given category by name
    @staticmethod
    def getDate(event_name):
        rows = app.db.execute('''
SELECT date
FROM Events
WHERE name = (:event_name)
''', event_name = event_name)
        return rows[0][0]

# method to get a given minElo by ID
    @staticmethod
    def getMinElo(event_name):
        rows = app.db.execute('''
SELECT minELO
FROM Events
WHERE name = (:event_name)
''', event_name = event_name)
        return rows[0][0]

# method to get a given maxElo by ID
    @staticmethod
    def getMaxElo(event_name):
        rows = app.db.execute('''
SELECT maxELO
FROM Events
WHERE  name = (:event_name)
''', event_name = event_name)
        return rows[0][0]

# method to get a given maxElo by ID
    @staticmethod
    def getType(event_name):
        rows = app.db.execute('''
SELECT type
FROM Events
WHERE  name = (:event_name)
''', event_name = event_name)
        return rows[0][0]


# method to get a given whole Event by name
    @staticmethod
    def getFromName(event_name):
        rows = app.db.execute('''
SELECT event_id,name,type,to_char(date,'Month DD, YYYY'),minELO,maxELO,category
FROM Events
WHERE name = :event_name
''', event_name = event_name)
        return [Events(*row) for row in rows]




# method to get a given the top 3 players in an Event by ID
    @staticmethod
    def get_top_three_players(event_id):
        rows = app.db.execute('''

SELECT T.match_id AS matchID, Matches.user1_ID AS user1_ID, Matches.user2_ID AS user2_ID, Matches.user1_score AS user1_score, Matches.user2_score AS user2_score, Matches.date_time AS date_time
                FROM(
                    SELECT match_id
                    FROM MatchInEvent
                    WHERE event_id = :event_id
                ) AS T, Matches
            WHERE Matches.matchID = T.match_id




''', event_id = event_id)
        return rows

    @staticmethod
    def get_all_in_event(event_id):
        rows = app.db.execute('''
SELECT Matches.activity, T.match_id AS match_id, Matches.user1_ID, Matches.user2_ID, Matches.user1_score, Matches.user2_score, Matches.date_time, Matches.accepted
FROM (
    SELECT match_id
    FROM MatchInEvent
    WHERE event_id = :event_id
) AS T, Matches
WHERE Matches.matchID = T.match_id
''', event_id = event_id
                              )
        return rows



    @staticmethod
    def get_relevant_from_event(event_id):
        rows = app.db.execute('''
          
       
SELECT D.activity AS activity, D.matchID AS matchID, D.name1 AS name1, Rankables.name AS name2, D.user1_score AS user1_score, D.user2_score AS user2_score, D.date_time AS date_time
        FROM
        (
            Rankables INNER JOIN
                (
               
        SELECT M.activity AS activity, M.matchID AS matchID, Rankables.name AS name1, M.user2_ID AS user2_ID, M.user1_score AS user1_score, M.user2_score AS user2_score, M.date_time AS date_time
        FROM
        (
            Rankables INNER JOIN
                (
                SELECT Matches.activity AS activity, T.match_id AS matchID, Matches.user1_ID AS user1_ID, Matches.user2_ID AS user2_ID, Matches.user1_score AS user1_score, Matches.user2_score AS user2_score, Matches.date_time AS date_time
                FROM(
                    SELECT match_id
                    FROM MatchInEvent
                    WHERE event_id = :event_id
                ) AS T, Matches
            WHERE Matches.matchID = T.match_id
            ) AS M
        ON Rankables.rankable_id = M.user1_ID)


            ) AS D
        ON Rankables.rankable_id = D.user2_ID)


''', event_id = event_id)
        return rows
        


    @staticmethod
    def getMaxUser1FromEvent(event_id, max):
        rows = app.db.execute('''
          SELECT Rankables.name AS name
        FROM
        (
            Rankables INNER JOIN
            
                (SELECT Matches.user1_ID AS user1_ID, Matches.user1_score AS user1_score
                FROM(
                    SELECT match_id
                    FROM MatchInEvent
                    WHERE event_id = :event_id
                ) AS T, Matches
            WHERE Matches.matchID = T.match_id) PART1
            ON Rankables.rankable_id = PART1.user1_ID AND PART1.user1_score = :max)
        

''', event_id = event_id, max = max)
        return rows


    @staticmethod
    def getMaxUser2FromEvent(event_id, max):
        rows = app.db.execute('''
          SELECT Rankables.name AS name
        FROM
        (
            Rankables INNER JOIN
            
                (SELECT Matches.user2_ID AS user2_ID, Matches.user2_score AS user2_score
                FROM(
                    SELECT match_id
                    FROM MatchInEvent
                    WHERE event_id = :event_id
                ) AS T, Matches
            WHERE Matches.matchID = T.match_id) PART1
            ON Rankables.rankable_id = PART1.user2_ID AND PART1.user2_score = :max)

''', event_id = event_id, max = max)
        return rows




    @staticmethod
    def getMax1(event_id):
        return app.db.execute('''
SELECT MAX(Matches.user1_score) AS user1_score
                FROM(
                    SELECT match_id
                    FROM MatchInEvent
                    WHERE event_id = :event_id
                ) AS T, Matches
            WHERE Matches.matchID = T.match_id
''', event_id = event_id)[0][0]


    @staticmethod
    def getMax2(event_id):
        return app.db.execute('''
SELECT MAX(Matches.user2_score) AS user2_score
                FROM(
                    SELECT match_id
                    FROM MatchInEvent
                    WHERE event_id = :event_id
                ) AS T, Matches
            WHERE Matches.matchID = T.match_id
''', event_id = event_id)[0][0]


    @staticmethod
    def getNumberOfMatches(event_id):
        return app.db.execute('''
SELECT COUNT(Matches.user1_score) AS myCount
                FROM(
                    SELECT match_id
                    FROM MatchInEvent
                    WHERE event_id = :event_id
                ) AS T, Matches
            WHERE Matches.matchID = T.match_id
''', event_id = event_id)[0][0]
