from tortoise import fields
from tortoise.models import Model

class User(Model):
    user_id = fields.IntField(pk=True)
    user_name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=150, unique=True, null=True)

    def __str__(self):
        return self.user_name