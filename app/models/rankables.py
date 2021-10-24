from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class Rankables(UserMixin):
    def __init__(self, rankable_id, email, name, category, about):
        self.rankable_id = rankable_id
        self.category = category
        self.name = name
        self.email = email
        self.about = about

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, rankable_id, email, name, category, about
FROM Rankables
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return Rankables(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Rankables
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, name, category, about):
        print(email)
        print(password)
        print(name)
        print(category)
        print(about)
        try:
            rows = app.db.execute("""
INSERT INTO Rankables(email, password, name, about, category)
VALUES(:email, :password, :name, :about, :category)
RETURNING rankable_id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  name=name,
                                  category=category,
                                  about=about)
            rankable_id = rows[0][0]
            print("what I need: "+str((Rankables.get(rankable_id)).category))
            return Rankables.get(rankable_id)
        except Exception as e:
            print(str(e))
            # likely email already in use; better error checking and
            # reporting needed
            return None

    @staticmethod
    @login.user_loader
    def get(rankable_id):
        rows = app.db.execute("""
SELECT rankable_id, email, name, category, about
FROM Rankables
WHERE rankable_id = :rankable_id
""",
                              rankable_id=rankable_id)
        
        return Rankables(*(rows[0])) if rows else None
