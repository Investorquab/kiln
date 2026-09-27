# Clean Container Contract

Kiln is designed to be demonstrable from a clean container.

## Services

- PostgreSQL 16
- FastAPI backend
- Next.js frontend

## Runtime

Application services communicate over the local Docker network. Runtime services should not require outbound internet access after images are built. Dependency installation happens during image build, not application startup.

PostgreSQL is an internal service; FastAPI uses port 8000 and Next.js uses port 3000.
The default Compose runtime network is internal-only. Services retain Compose DNS-based
connectivity to each other, while the backend and frontend ports remain published to the host.

The final submission must publish the actual CPU, memory, and concurrency limits used for the recorded run. Do not treat local development capacity as a claimed benchmark.

The clean-container demonstration should show images build, services start, the health endpoint responds, verification attacks run, and the same verification command can be repeated without previous run state.