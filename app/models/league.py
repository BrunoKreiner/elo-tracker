from flask import current_app as app


class League:
    def __init__(self, l_id, name, president):
        self.l_id = l_id
        self.name = name
        self.president = president

    @staticmethod
    def get(name):
        rows = app.db.execute('''
SELECT name
FROM Activity
WHERE name = :name
''',
                              name=name)
        return Activity(*(rows[0])) if rows is not None else None