from flask import current_app as app

class Leagues:
    
    def __init__(self, l_id, name, president):
        self.l_id = l_id
        self.name = name
        self.president = president

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT l_id, name, president
FROM League
''')
        return [Leagues(*row) for row in rows]



    # add a new league.
    @staticmethod
    def addLeague(name, president): # what were the try-except blocks for?

        maxLeagueID = app.db.execute("""
SELECT MAX(l_id)
FROM League;
"""
                                  )[0][0]


            
        
        rows = app.db.execute("""
INSERT INTO League(l_id, name, president)
VALUES(:l_id, :name, :president)
RETURNING l_id
""", l_id=maxLeagueID + 1, name=name, president=president)
        l_id = rows[0][0] # why do we want to return the first name?
        return l_id
       