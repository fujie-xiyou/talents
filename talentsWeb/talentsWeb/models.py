from mongoengine import fields
from mongoengine import Document


# 记录自增键
class AI(Document):
    _id = fields.StringField()
    seq = fields.IntField(default=1)


class User(Document):
    user_id = fields.IntField()
    username = fields.StringField(max_length=50)
    phone = fields.StringField(max_length=11)
    email = fields.StringField(max_length=50)
    password = fields.StringField(max_length=35)


class Test(Document):
    _id = fields.StringField(primary_key=True)
    test = fields.StringField()