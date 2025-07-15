from tortoise import fields
from tortoise.models import Model

class Doctor(Model):
    doctor_id = fields.IntField(pk=True)
    doctor_name = fields.CharField(max_length=100)
    speciality = fields.CharField(max_length=100, null=True)

    def __str__(self):
        return self.doctor_name