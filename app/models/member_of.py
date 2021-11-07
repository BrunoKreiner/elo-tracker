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


#     @staticmethod # get the leagues the logged in user is a member of.
#     def get_user_leagues():
#         rows = app.db.execute('''
# SELECT l_id, user_id, status
# FROM Member_of
# ''') # WHERE user_id = {{current_user.name}}
#         return [Member_of(*row) for row in rows]


    @staticmethod # get the leagues the logged in user is a member of.
    def get_user_leagues(rankable_id):
        rows = app.db.execute('''
SELECT l_id, user_id, status
FROM Member_of
WHERE user_id = :rankable_id
''', rankable_id = rankable_id) # WHERE user_id = {{current_user.name}}
        return [Member_of(*row) for row in rows]

    # add a new Member_of.
    @staticmethod
    def addMember(l_id, user_id, status): 
        rows = app.db.execute("""
INSERT INTO Member_of(l_id, user_id, status)
VALUES(:l_id, :user_id, :status)
RETURNING l_id
""", l_id=l_id, user_id=user_id, status=status)
        l_id = rows[0][0]
        return l_id