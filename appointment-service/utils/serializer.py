# utils/serializer.py

import json
from proto import appointment_pb2

def serialize_list(slots):
    """Convert list of slot dicts or Tortoise objects to gRPC AppointmentList"""
    return appointment_pb2.AppointmentList(
        appointments=[
            appointment_pb2.AppointmentSlot(
                slot_id=slot.slot_id,
                doctor_id=slot.doctor_id,
                appointment_date=str(slot.appointment_date),
                time=slot.time,
                available=slot.available
            )
            for slot in slots
        ]
    )

def serialize_for_cache(slots):
    """Convert to JSON-serializable list for Redis"""
    return json.dumps([
        {
            "slot_id": slot.slot_id,
            "doctor_id": slot.doctor_id,
            "appointment_date": str(slot.appointment_date),
            "time": slot.time,
            "available": slot.available
        }
        for slot in slots
    ])

def deserialize_list(json_str):
    """Convert JSON string from Redis back into list of dicts"""
    return json.loads(json_str)