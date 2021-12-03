from flask import current_app as app

class MatchInEvent:
    
    def __init__(self, matchID,eventID):
        self.matchID = matchID
        self.eventID = eventID

    @staticmethod
    def addMatchAndEvent(event, matchID):

        if (len(event)> 0):
            eventID = app.db.execute("""
SELECT event_id
FROM Events
WHERE name = :event
""", event = event)
            if (len(eventID) == 0):
                    return

            eventID = eventID[0][0]
            if(len(event) > 0):
                rows = app.db.execute("""
    INSERT INTO MatchInEvent(match_id,event_id)
    VALUES(:matchID, :eventID)
    RETURNING event_id
    """,
                                    matchID=matchID,
                                    eventID = eventID
                                    )
            eventID = rows[0][0]
        
            
            
            return eventID
       
    