from flask import current_app as app


class Activity:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT name
FROM Activity
''')
        return [Activity(*row) for row in rows]
        