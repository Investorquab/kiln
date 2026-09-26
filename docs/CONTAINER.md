# Clean Container Contract

Kiln is designed to start from a clean container with no dependency on the host application state.

## Services
- PostgreSQL 16
- FastAPI backend
- Next.js demonstration frontend

## Published local ports
- 5432 — PostgreSQL
- 8000 — backend
- 3000 — frontend

## Resource notes
The hackathon environment must publish the actual CPU, memory, and concurrency limits used for the final run. Do not claim limits that have not been measured or configured.

## Network boundary
The application itself should not require outbound network access for the clean-room workload. Dependencies are installed during image build; the runtime path is local to the compose network.
