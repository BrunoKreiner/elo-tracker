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


# add a new activity.
    @staticmethod
    def addActivity(name): # what were the try-except blocks for?
        rows = app.db.execute("""
INSERT INTO Activity(name)
VALUES(:name)
RETURNING name
""", name=name)
        name = rows[0][0] # why do we want to return the first name?
        return name

