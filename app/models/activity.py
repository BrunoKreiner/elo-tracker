from flask import current_app as app


class Activity:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def get(name):
        rows = app.db.execute('''
SELECT name
FROM Activity
WHERE name = :name
''',
                              name=name)
        return Activity(*(rows[0])) if rows is not None else None