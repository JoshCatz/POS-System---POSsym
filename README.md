# POSsym - Restaurant Point of Sale System 

A full-stack POS system built for restaurants. Designed to run locally on a Beelink Mini PC per location, with hourly sync to AWS for analytics, payroll, and reporting.

## Tech Stack 
Frontend - React -> Tablet POS interface and kitchen monitors
API - FastAPI + Uvicorn -> REST API and Websocket server
ORM - SQLAlchemy 2.0 (async) -> Database interactions
Database - PostreSQL 17 -> Source of truth database
Cache/Messaging - Redis 7 -> Table locking, kitchen pub/sub, job queue
Background Jobs - Celery + Celery Beat -> AWS batch sync, payroll, schedueled tasks
Payments - Stripe Terminal -> Tableside card processing
Cloud - AWS (RDS, S3, ECS, Lambda) -> Analytics, reporting, backups
Containers - Docker + Docker Compose -> Local Developement/Deployment

## Prerequisites
Install these before anything else!
- Docker Desktop - runs all services
- Git - version control
- VS Code - RECOMMENEDED editor (can use personal preference)

+ You do not need Python, PostgreSQL, or Redis installed locally! Everything runs from in the Docker containers

## Getting Started 
### 1. Clone the repo:
    ```bash
    git clone https://github.com/your-org/POS-System---POSsym.git
    cd POS-System---POSsym
    ```

### 2. Create Your Environment File
    ```bash
    cp .env.example .env
    ```
    
(copies .env.example to a new file -> .env)
Open .env and fill with your local values:
    ```bash
    # Database
    DATABASE_URL=postgresql+asyncpg://example:example@db:5432/pos_db

    # Redis
    REDIS_URL=redis://redis:6379

    # Auth
    JWT_SECRET=anylocalstringwilldo

    # Environment
    ENVIRONMENT=development
    DEBUG=true
    ```

Never commit .env to Git! Its already in .gitignore so you shouldn't have to worry about it.

### 3. Start up
```bash
docker compose up --build
```

### 4. Confirm everything is running
In a second terminal
```bash
docker compose ps
```
Should show all the services running

### 5. Confirm the API is running
```bash
curl http://localhost:8000/health
```

## Project Structure
/POS-System---POSsym
  docker-compose.yml          ← starts all services
  .env                        ← your local secrets (never committed)
  .env.example                ← template for teammates
  README.md

  /backend
    Dockerfile                ← builds the API image
    requirements.txt          ← Python dependencies
    seed.py                   ← populates database with test data

    /app
      main.py                 ← FastAPI entry point
      workers.py              ← Celery configuration
      /api                    ← route handlers
      /models                 ← SQLAlchemy models (database tables)
      /schemas                ← Pydantic request/response shapes
      /services               ← business logic
      /workers                ← Celery background tasks

    /migrations               ← Alembic migration files
    /tests                    ← pytest test suite

  /frontend                   ← React application (coming soon)
  /docs                       ← API contracts, WebSocket event schema

### Usefule Commands
```bash
# Start everything (first time or after code changes)
docker compose up --build

# Start everything (normal, no rebuild)
docker compose up

# Stop everything cleanly (data is preserved)
docker compose down

# Stop everything and wipe all data (fresh start)
docker compose down -v
```

### Debugging
```bash
# Check container status
docker compose ps

# View logs for a specific service
docker compose logs api
docker compose logs db
docker compose logs celery_worker

# Follow logs in real time
docker compose logs -f api

# Shell into the API container
docker compose exec api bash

# Run a command inside the API container
docker compose exec api python seed.py
docker compose exec api alembic upgrade head
docker compose exec api pytest
```

### Database
```bash
# Connect to PostgreSQL directly
docker compose exec db psql -U example -d pos_db

# List all tables
\dt

# Quit psql
\q
```

### Redis

```bash
# Ping Redis
docker compose exec redis redis-cli ping
# Expected: PONG

# Open Redis CLI
docker compose exec redis redis-cli
```

### Architecture Overview
```bash
[ELO Tablets - React]
        |
    WiFi (isolated VLAN)
        |
[Beelink Mini PC - Local Hub]
   ├── FastAPI (REST + WebSockets)  :8000
   ├── PostgreSQL (source of truth) :5432
   ├── Redis (locks + pub/sub)      :6379
   └── Celery + Beat (background jobs)
        |                |
[Kitchen Monitors]   Hourly Batch Sync
   (wired)                |
                     [AWS Cloud]
                     ├── RDS (PostgreSQL)
                     ├── S3 (storage/backups)
                     ├── ECS/Fargate (services)
                     └── CloudWatch (monitoring)
```