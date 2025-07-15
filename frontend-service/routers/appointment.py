# Defines /appointments REST endpoints that internally call the gRPC client stub.
from fastapi import APIRouter
from grpc_clients.appointment_stub import stub
from proto import appointment_pb2

router = APIRouter()

@router.get("/appointments/")
async def get_available_appointments(doctor_id: str, date: str):
    request = appointment_pb2.AppointmentRequest(doctor_id=doctor_id, date=date)
    response = await stub.FetchAvailableAppointments(request)
    return {"appointments": [apt for apt in response.appointments]}


@router.post("/appointments/book/")
async def make_appointment( slot_id: str, user_id: str):
    request = appointment_pb2.BookAppointmentRequest(slot_id, user_id)
    response = await stub.RequestAppointmentBooking(request)
    return {"success": response.success, "message": response.message}


@router.post("/appointments/cancel/")
async def cancel_appointment(slot_id: str):
    req = appointment_pb2.CancelAppointmentRequest(slot_id=slot_id)
    res = await stub.RequestAppointmentCancellation(req)
    return {"success": res.success, "message": res.message}






