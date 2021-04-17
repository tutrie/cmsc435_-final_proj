import db

class User:
    username = db.StringField(required=True, unique=True, min_length=1, max_length=20)
    password = db.StringField(required=True, min_length=1, max_length=20)

    # Returns unique string identifying our object
    def get_id(self):
        return self.username
