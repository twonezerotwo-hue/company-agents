# Company Agents API

Docker ile çalışan FastAPI projesi.

## Kurulum

\\\ash
docker-compose up -d
\\\

## API Endpoints

- GET \/\ - Welcome
- GET \/health\ - Health check
- POST \/agents/run\ - Run agent

## Services

- **API:** FastAPI (8080)
- **Database:** PostgreSQL (5432)
- **Redis:** Cache (6379)
- **Agents:** Crew Agents