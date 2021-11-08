from flask import current_app as app

class Events:
    
    def __init__(self, event_id, name, type,date):
        self.event_id = event_id
        self.name= name
        self.type =type
        self.date =date


    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT event_id, name, type,date
FROM Events
''')
        return [Events(*row) for row in rows]

  # define method to add an event     

    



