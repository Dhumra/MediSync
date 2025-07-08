# 🏥 MediSync: Distributed Healthcare Microservice System

In this project, you'll build a **fault-tolerant, replicated healthcare microservice system** that supports appointment booking, medication issuing, and inventory synchronization across clinics. The design emphasizes **caching, consistency, scalability, and crash fault tolerance**.

---

## 💡 Lab Description

Healthcare IT systems often suffer from:

- High latency in scheduling
- Fragile inventory coordination
- Downtime due to centralized failures

To solve these challenges, you will build a **distributed healthcare backend** using **Python 3.11+**, **gRPC**, **Redis**, and **PostgreSQL**, with modern architecture features:

- Microservices
- Caching with invalidation
- Leader-based replication and failover
- Service discovery and orchestration

This system will consist of several independently deployable microservices, running as Docker containers, and deployed on AWS.

---

## 🔧 System Overview

| **Microservice**        | **Responsibilities**                                                                           |
|-------------------------|-----------------------------------------------------------------------------------------------|
| `client-service`        | Simulates client behavior and generates REST/gRPC requests                                    |
| `frontend-service`      | Receives REST API calls, validates input, and routes to backend services via gRPC            |
| `appointment-service`   | Manages appointment booking, cancellation, and slot caching                                   |
| `medication-service`    | Issues prescriptions after appointment booking                                               |
| `inventory-service`     | Manages medicine stock, replicates updates across clinics (leader-follower replication)       |
| `notification-service`* | Sends appointment and prescription confirmations via async queue (optional)                   |

All services communicate using **gRPC with Protobuf**, and leverage **PostgreSQL** and **Redis** for persistence and caching.

---

## 📦 Part 1: Caching

To reduce latency during high-load appointment lookups, the system implements **multi-layer caching** in `appointment-service`.

✅ **Caching Flow:**

1. `frontend-service` makes a gRPC call to `appointment-service`.
2. `appointment-service` checks **in-memory LRU cache** (`functools.lru_cache` or similar).
3. If not found, it checks **Redis cache** (`aioredis`).
4. If still missing, it queries PostgreSQL, returns results, and updates both caches.

✅ **Cache Invalidation:**

- When an appointment is booked or canceled, the relevant slot is invalidated in Redis and in-memory caches.
- Uses either **Redis Pub/Sub** or direct cache invalidation.
- **LRU eviction policy** automatically evicts least-recently-used entries when the cache exceeds configured size.

✅ **Configuration:**

- Cache size: Configurable via environment variables or config files.
- Replacement policy: LRU.
- Consistency: No stale slots returned.

---

## 🔁 Part 2: Replication

The `inventory-service` is replicated across multiple clinics with **one leader and multiple followers**.

✅ **Replication Flow:**

- `frontend-service` identifies the leader at startup (manual config or Redis key).
- All write operations (stock deductions) go through the leader.
- Leader propagates writes to followers via gRPC broadcast.
- Each replica uses its own PostgreSQL DB for persistence.

✅ **Bootstrapping:**

- Each replica starts with a unique ID.
- Leader selection can be:
  - Manual config (e.g., `LEADER_ID=1`), or
  - Redis key with TTL (automatic leader election).

✅ **Replication Queue:**

- Use **Redis Streams** or **RabbitMQ** (`aio-pika`) for async replication.

---

## 💥 Part 3: Fault Tolerance

To maintain high availability:

✅ **Leader Failover:**

- If `frontend-service` detects an unresponsive leader:
  - Marks it dead.
  - Elects the next-highest-ID replica as the new leader.
  - Broadcasts leader change to all replicas.
  - Updates Redis registry (if used).

✅ **Replica Recovery:**

- When a crashed replica restarts:
  - Queries the current leader for missed stock updates.
  - Replays updates to reach consistent state.
  - Rejoins as follower transparently.

---

## 🧪 Part 4: Testing and Deployment

✅ **Local Testing:**

- **Unit testing:** `pytest` for all microservices.
- **Integration testing:** Postman or `curl` for REST APIs.
- **gRPC testing:** `grpclib.testing`.
- **Load testing:** `k6` or `Locust` for concurrency simulations.

✅ **Deployment:**

- Local: `docker-compose up --build`
- Cloud: Fly.io or Render (`fly launch`)
- Each microservice runs in its own container with environment-based configs.

---

## 📊 Evaluation Metrics

Measure and demonstrate:

- Average slot query time with and without caching.
- Failover time when leader crashes.
- Consistent state replication after recovery.
- LRU cache evictions (sample logs).

---

## 🧠 Optional (Extra Credit): Distributed Consensus

Implement a **Raft-style consensus protocol** to:

- Guarantee strong consistency in stock replication.
- Ensure all replicas apply updates in the same order.
- Support automatic leader election without manual intervention.

---

## 🧰 Finalized Technology Stack

| **Layer**             | **Recommended Tech**                               | **Why This Works**                                                        |
|-----------------------|----------------------------------------------------|---------------------------------------------------------------------------|
| Language/Runtime      | Python 3.11+ with `FastAPI` and `grpclib`          | Async, modern, expressive; FastAPI for REST gateway                      |
| Inter-service Comm    | gRPC + Protobuf                                    | High performance, contract-first APIs                                    |
| Database              | PostgreSQL (`asyncpg` or async `SQLAlchemy`)       | Robust transactions, relational model                                    |
| Caching               | Redis (`aioredis`) + in-memory LRU                 | Fast reads, TTLs, invalidation                                           |
| Replication Queue     | Redis Streams or RabbitMQ (`aio-pika`)             | Async replication and eventing                                           |
| Service Discovery     | Redis TTL registry or Consul                       | Simple TTL-based leader tracking; scalable for production                |
| Orchestration         | Docker Compose (local), Fly.io or AWS for deployment | Easy containerization and scaling                                        |
| Monitoring (optional) | Prometheus + Grafana or stdout logs                | Observe gRPC metrics, cache hit rates, and errors                        |
| Testing               | `pytest`, `grpclib.testing`, Postman               | Comprehensive unit and integration testing                               |
| Load Testing          | `k6` CLI                                           | Simulate load and concurrency for performance validation                |

---

## 🧾 Deliverables

| **Item**             | **Description**                                                |
|----------------------|----------------------------------------------------------------|
| `README.md`          | Project overview, setup, and test instructions                |
| `docker-compose.yml` | Service orchestration for local deployment                    |
| `proto/`             | `.proto` definitions for all gRPC services                    |
| `test/`              | Unit and integration test scripts                             |
| `logs/`              | Sample logs demonstrating cache eviction and failover         |
| `deployment/`        | Scripts for Fly.io or AWS deployment                          |

---

## ✅ How to Present (Resume / Portfolio)

> Designed a fault-tolerant microservice system for healthcare scheduling and medication distribution using Python 3.11+, gRPC APIs, Redis-backed caching, and leader-based replication. Implemented automatic failover and recovery workflows to achieve high availability and low-latency responses under load.


