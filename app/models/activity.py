from flask import current_app as app

class Activity:
    def __init__(self, name, category):
        self.name = name
        self.category = category

    @staticmethod
    def get(name):
        rows = app.db.execute('''
SELECT *
FROM Activity
WHERE name = :name
''',
            name=name)
        return [Activity(*row) for row in rows]


    @staticmethod
    def get_valid_category():
        rows = app.db.execute('''
SELECT distinct category
FROM Activity
''')
        return [row[0] for row in rows]


    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT name, category
FROM Activity
''')
        return [Activity(*row) for row in rows]



# add a new activity.
    @staticmethod
    def addActivity(name, category): # what were the try-except blocks for?
        rows = app.db.execute("""
INSERT INTO Activity(name, category)
VALUES(:name, :category)
RETURNING name
""", name=name, category=category)
        name = rows[0][0] # why do we want to return the first name?
        return name

    @staticmethod
    def get_category(name):
        rows = app.db.execute('''
SELECT category
FROM Activity
WHERE name = :name
''',
                name=name)
        return rows[0][0]

    @staticmethod
    def get_name(name):
        rows = app.db.execute('''
SELECT name
FROM Activity
WHERE name = :name
''',
                name=name)
        return rows
