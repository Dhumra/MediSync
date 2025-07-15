# grpc_clients/appointment_stub.py
import grpc
from grpc_clients import appointment_pb2_grpc

channel = grpc.aio.insecure_channel("localhost:50051")  # Port must match your appointment-service
stub = appointment_pb2_grpc.AppointmentFrontendBridgeStub(channel)