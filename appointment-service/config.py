import os
from dotenv import load_dotenv

# Load environment variables from .env file at project root
load_dotenv()

# Database
POSTGRES_URI = os.getenv("POSTGRES_URI", "postgresql://user:password@localhost:5432/medisync")

# Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Cache
CACHE_MAX_SIZE = int(os.getenv("CACHE_MAX_SIZE", 100))  # For in-memory LRU cache
CACHE_TTL = int(os.getenv("CACHE_TTL", 300))            # For Redis cache (in seconds)

# App
SERVICE_NAME = os.getenv("SERVICE_NAME", "appointment-service")


# How to use 
# import asyncpg
# from config import POSTGRES_URI
# conn = await asyncpg.connect(POSTGRES_URI)