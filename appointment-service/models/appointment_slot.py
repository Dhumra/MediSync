from tortoise import fields
from tortoise.models import Model
from models.user import User
from models.doctor import Doctor

class AppointmentSlot(Model):
    slot_id = fields.IntField(pk=True)
    doctor = fields.ForeignKeyField("models.Doctor", related_name="slots", on_delete=fields.CASCADE)
    appointment_date = fields.DateField()
    appointment_time = fields.TimeField()
    is_available = fields.BooleanField(default=True)
    booked_by_user = fields.ForeignKeyField("models.User", related_name="appointments", null=True, on_delete=fields.SET_NULL)

    class Meta:
        unique_together = ("doctor", "appointment_date", "appointment_time")

    def __str__(self):
        return f"{self.doctor} - {self.appointment_date} {self.appointment_time}"