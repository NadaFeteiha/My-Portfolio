from peewee import *
from datetime import datetime
from app.database import mydb

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    image = CharField(null=True)  
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = mydb
