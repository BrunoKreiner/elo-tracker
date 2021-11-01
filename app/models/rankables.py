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
            print("wrong password")
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
    def updateEmail(rankable_idNew, emailNew):
        try:
            rows = app.db.execute("""
UPDATE Rankables
SET email = :emailNew
WHERE rankable_id = :rankable_idNew
RETURNING rankable_id;
""",
                                  emailNew=emailNew,
                                  rankable_idNew=rankable_idNew
                                  )
            return True
        except Exception as e:
            print(str(e))
            return False

    @staticmethod
    def updateName(rankable_idNew, nameNew):
        try:
            rows = app.db.execute("""
UPDATE Rankables
SET name = :nameNew
WHERE rankable_id = :rankable_idNew
RETURNING rankable_id;
""",
                                  nameNew=nameNew,
                                  rankable_idNew=rankable_idNew
                                  )
            return True
        except Exception as e:
            print(str(e))
            return False

    @staticmethod
    def updateCategory(rankable_idNew, categoryNew):
        try:
            rows = app.db.execute("""
UPDATE Rankables
SET category = :categoryNew
WHERE rankable_id = :rankable_idNew
RETURNING rankable_id;
""",
                                  categoryNew=categoryNew,
                                  rankable_idNew=rankable_idNew
                                  )
            return True
        except Exception as e:
            print(str(e))
            return False

    @staticmethod
    def updatePassword(rankable_idNew, passwordNew):
        try:
            rows = app.db.execute("""
UPDATE Rankables
SET password = :passwordNew
WHERE rankable_id = :rankable_idNew
RETURNING rankable_id;
""",
                                  passwordNew=generate_password_hash(passwordNew),
                                  rankable_idNew=rankable_idNew
                                  )
            return True
        except Exception as e:
            print(str(e))
            return False

    @staticmethod
    def updateAbout(rankable_idNew, aboutNew):
        try:
            rows = app.db.execute("""
UPDATE Rankables
SET about = :aboutNew
WHERE rankable_id = :rankable_idNew
RETURNING rankable_id;
""",
                                  aboutNew=aboutNew,
                                  rankable_idNew=rankable_idNew
                                  )
            return True
        except Exception as e:
            print(str(e))
            return False

    @staticmethod
    def register(email, password, name, category, about):
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

    @staticmethod
    def get_all_visible():
        rows = app.db.execute('''
SELECT rankable_id, email, name, category, about
FROM Rankables
''')
        return [Rankables(*row) for row in rows]
