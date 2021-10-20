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