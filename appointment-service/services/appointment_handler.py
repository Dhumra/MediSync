# # appointment-service/service/appointment_handler.py :Implements gRPC service methods defined in appointment.proto. Uses db/, cache/, and models/ to process requests.

# Import Db and redis , lru cache

from cache.memory_cache import lru_cache
from cache.redis_cache import redis_cache
from utils.serializer import serialize_list, deserialize_list
from models import AppointmentSlot
from proto import appointment_pb2, appointment_pb2_grpc
from cache.invalidator import invalidateCache


class AppointmentService(appointment_pb2_grpc.AppointmentServiceServicer):

    async def LookupAppointment(self, req, context):
        # Fistst checks cache, then redis cont then db container
        # in request we get doctor_id and dat
        doctor_id = req.doctor_id
        date = req.date
        cache_key = (doctor_id, date)

        # 1️⃣ Check LRU Cache
        result = lru_cache.get(cache_key)

        if result:
            return serialize_list(result)

         # 2️⃣ Check Redis Cache
        result_json = await redis_cache.get(cache_key)

        if result_json:
            result = deserialize_list(result_json)
            lru_cache.put(cache_key, result)
            return serialize_list(result)

        # 3️⃣ Fallback: Fetch from DB
        result = await AppointmentSlot.filter(doctor_id = doctor_id, appointment_date = date ).all()

        if not result:
            # Return empty list if no slots
            return appointment_pb2.AppointmentList(appointments=[])
        

        invalidateCache(doctor_id, date)
        # lru_cache.put(cache_key, result)
        
        # await redis_cache.set(cache_key, serialize_list(result))
          


        return appointment_pb2.AppointmentList(serialize_list(result))


    async def BookAppointment(self, req, context):
        #Gets slot_id and user_id as request
        slot_id = req.slot_id
        user_id = req.user_id

        # Update the data id Postgres dB ND RENOVE CORRESONDING DATA FROM Cache
        slot = await AppointmentSlot.get(slot_id = slot_id).prefetch_related("doctor")
        slot.is_available = False
        slot.booked_by_user = user_id
        await slot.save()

        date = str(slot.appointment_date)
        doctor_id = slot.doctor.doctor_id
        cache_key = (doctor_id, date)

        invalidateCache(doctor_id, date)

        # lru_cache.remove(cache_key)
        # await redis_cache.delete(cache_key)
        
        return appointment_pb2.Confirmation(success=True, message="Appointment booked successfully.")

    async def CancelAppointment(self, req, context):
        # gETS SLOT_IDD AS req
        slot_id = req.slot_id

        slot = await AppointmentSlot.get(slot_id = slot_id).prefetch_related("doctor")   
        slot.is_available = True
        slot.booked_by_user = None
        await slot.save()
        # update(is_available = "True")
        
        date = str(slot.appointment_date)
        doctor_id = slot.doctor.doctor_id
        cache_key = (doctor_id, date)

        invalidateCache(doctor_id, date)

        # lru_cache.remove(cache_key)
        # await redis_cache.delete(cache_key)
        

        # Update the data id Postgres dB ND RENOVE CORRESONDING DATA FROM CCHE
        return appointment_pb2.Confirmation(success=True, message="Appointment cancelled successfully.")

