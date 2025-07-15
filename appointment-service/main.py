# Starts the gRPC server for this service. Registers appointment service handlers.
import asyncio
from config import POSTGRES_URI
from tortoise import Tortoise, run_async
from cache.subscriber import start_redis_subscriber
import grpc
from proto import appointment_pb2_grpc
from services.appointment_handler import AppointmentServiceHandler


async def init_db():
    await Tortoise.init(
        db_url=POSTGRES_URI,
        modules={"models": ["models"]}
    )
    await Tortoise.generate_schemas()





async def serve():
    await init_db()

    asyncio.create_task(start_redis_subscriber())

    server = grpc.aio.server()
    appointment_pb2_grpc.add_AppointmentServiceServicer_to_server(
        AppointmentServiceHandler(), server
    )
    server.add_insecure_port('[::]:50051')
    # Appointment service will reiceve a grpc call from front-end service
    print("✅ appointment-service gRPC server running on port 50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    run_async(serve())