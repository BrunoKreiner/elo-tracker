from flask import current_app as app

class Member_of:
    
    def __init__(self, l_id, user_id, status):
        self.l_id = l_id
        self.user_id = user_id
        self.status = status

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT l_id, user_id, status
FROM Member_of
''')
        return [Member_of(*row) for row in rows]


    @staticmethod # get the leagues the logged in user is a member of.
    def get_user_leagues():
        rows = app.db.execute('''
SELECT l_id, user_id, status
FROM Member_of
''') # WHERE user_id = {{current_user.name}}
        return [Member_of(*row) for row in rows]