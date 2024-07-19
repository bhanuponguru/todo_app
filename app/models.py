from flask_mongoengine import MongoEngine

db = MongoEngine()


class User(db.Document):
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    email = db.EmailField(required=True)
    password = db.StringField(required=True)


class Event(db.Document):
    title = db.StringField(required=True)
    description = db.StringField(required=True)
    due = db.DateTimeField(required=True)
    user_id = db.ObjectIdField(required=True)
