import flask_mongoengine as mgo
from mongoengine import Document, StringField, IntField


class User(mgo.Document):
    name = StringField(unique=True)
    fname = StringField()
    lname = StringField()
    email = StringField()
    student_id = StringField()
    wallet = IntField()
    reputation = IntField()
    numtrans = IntField()
    image = StringField()
    googleid = StringField()
    gaveto = StringField()

    meta = {
        'ordering': ['+lname','+fname']
    }
