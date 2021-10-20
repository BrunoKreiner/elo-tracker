from flask import current_app as app


class League:
    def __init__(self, l_id, name, president):
        self.l_id = l_id
        self.name = name
        self.president = president

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT *
FROM League
''')
        return League(*(rows[0])) if rows is not None else None