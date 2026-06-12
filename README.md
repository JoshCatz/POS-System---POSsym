# POSsym - Restaurant Point of Sale System 

A full-stack POS system built for restaurants. Designed to run locally on a Beelink Mini PC per location, with hourly sync to AWS for analytics, payroll, and reporting.

## Tech Stack 
### Frontend
- React -> Tablet POS interface and kitchen monitors
### API 
- FastAPI + Uvicorn -> REST API and WebSocket server
### ORM 
- SQLAlchemy 2.0 (async) -> Database interactions
### Database 
- PostgreSQL 17 -> Source of truth database
### Cache/Messaging 
- Redis 7 -> Table locking, kitchen pub/sub, job queue
### Background Jobs 
- Celery + Celery Beat -> AWS batch sync, payroll, scheduled tasks
### Payments (subject to change)
- Stripe Terminal -> Tableside card processing
### Cloud 
- AWS (RDS, S3, ECS, Lambda) -> Analytics, reporting, backups
### Containers 
- Docker + Docker Compose -> Local Development/Deployment

## Stack components explained

### Frontend: React

React is responsible for the user-facing POS interface. React will be responsible for powering the POS interface, and the monitor interface.

Typical responsibilities React handles:

* Redering menus, tables, checks, orders, and tickets
* Managing LOCAL UI state
* Sending HTTP requests to the FastAPI backend
* Opening WebSocket connections for real-time updates
* Displaying payment status from payment processing terminals
* Handling loading, error, and offline-like states

---

### API Layer: FastAPI + Uvicorn

FastAPI handles all incoming requests from the React frontend, validates data, runs business logic, interacts with the database through SQLAlchemy, communicates with Redis when needed, and returns structured responses to the frontend.

Uvicorn is the Asynchronous Server Gateway Interface (ASGI). Uvicorn is the process that receives network traffic and passes it into the FastAPI app. It supports asynchronous request handling and long-running WebSocket connections, which are important for real-time features.

Typical responsiblities handled in the API layer:

* REST API endpoints
* WebSocket endpoints
* Request validation
* Authentication and authorization
* Business rules
* Payment flow coordination
* Database transaction coordination
* Dispatching background jobs to Celery (explained below)

The API layer acts as the central coordinator of the application. The frontend should NOT need to know how payments, locks, database transactions, or background jobs work interanlly; it simply asks the backend to perform these tasks via HTTP requests to FastAPI.

---

### ORM Layer: SQLAlchemy 2.0 Async

SQLAlchemy is the database access layer. It maps python classes to database tables and lets the application query, insert, update, and delete data using Python objects rather than writing raw SQL everywhere.

In this project, SQLAlchemy 2.0 is used in async mode. This works well with FastAPI because FastAPI can handle asynchronous request/response cycles. Async database access allows the API server to keep handling other requests while waiting for the database to respond.

Typical responsibilities handled by SQLAlchemy:

* Defining database models
* Managing database sessions
* Creating queries
* Running inserts, updates, and deletes
* Managing transactions
* Mapping rows from PostgreSQL into Python objects

The ORM layer is important because it keeps database logic organized and reusable. Instead of every endpoint manually building SQL strings, the application can centralize model definitions and query patterns.

---

### Database: PostgreSQL 17

PostgreSQL is the system's "source of truth". This means it is the authoritative storage layer for durable business data.

If Redis is cleared, a container restarts, a WebSocket disconnects, or a worker fails, PostgreSQL should still contain the official record of restaurants, users, menu items, orders, checks, payments, shifts, and audit logs.

PostgreSQL stores data such as:

* Restaurants and locations
* Users, roles, and permissions
* Tables and seating areas
* Menu categories and menu items
* Menu items
* Orders and order items
* Kitchen tickets
* Checks and split checks
* Payments and refunds
* Discounts, taxes, and service charges
* Employee shifts
* Payrool records
* Reports and analytics records
* Audit logs

PostgreSQL is especially significant because all business data must be durable and consistent. For example, once a payment is completed, the system needs a reliable record of what was paid, when it was paid, who processed it, and which order/check it belonged to.

---

### Cache and Messaging: Redis 7

Redis is used for fast, temporary, real-time coordination. It is not the primary database. Instead, it supports features that need to be extremely fast or event-driven.

In this system, Redis has THREE primary jobs:

* Table locking (don't let 2 users access the same table simulataneously)
* Kitchen pub/sub messaging (allows one part of the system to publish an event while another receives it)
* Job queue / broker for Celery (Establish a line of tasks to be completed by Celery worker)

---

### Background jobs: Celery + Celery Beat

Celery handles background jobs. These are tasks that should not block the main API request/response cycle. For example, when a manager clicks "Generate Payroll Report", the API should not freeze while the report is built. Instead, FastAPI can enqueue a Celery task and immediately return a response saying the job has started.

Typical Celery responsiblities include:

* Long-running jobs
* Retryable tasks
* Report generation
* AWS sync jobs
* Payroll calculations
* Processing analytics
* Cleanup tasks

Celery Beat is the scheduler. It triggers tasks to be performed in order on a schedule. For example, You want to sync sales data to AWS every 15 minutes, you want to generate a nightly report at 2:00 AM, You want to run payroll calculations every Monday, You want to archive old tickets nightly, etc.

---

### Containers: Docker + Docker compose

Docker packages each part of the system into containers. This makes the app easier to run consistently across developer machines and deployment environments.

Docker compose defines and runs multiple services together.

For local development, Docker Compose may start:

* React frontend
* FastAPI backend
* PostgreSQL database
* Redis server
* Celery worker
* Celery Beat scheduler
        
## How the stack interacts

### Starting the System locally:

```text
Developer runs docker compose up 
            | 
Docker starts frontend, api, db, redis, worker, and beat containers 
            | 
React becomes available in the browser/tablet 
            | 
FastAPI starts under Uvicorn 
            | 
PostgreSQL stores local development data 
            | 
Redis becomes available for locks, pub/sub, and task queue 
            | 
Celery worker waits for jobs 
            | 
Celery Beat waits to trigger scheduled jobs
```

        

## Prerequisites
Install these before anything else!
- Docker Desktop - runs all services
- Git - version control
- VS Code - RECOMMENDED editor (can use personal preference)

+ You do not need Python, PostgreSQL, or Redis installed locally! Everything runs inside the Docker containers

## Development Philosophy

- Main should always remain deployable.
- No direct pushes to main.
- Every change goes through a Pull Request.
- At least one approval is required before merge.
- Communicate major architectural changes before implementation.

## Getting Started 
### 1. Clone the repo:
    ```bash
    git clone https://github.com/your-org/POS-System---POSsym.git
    cd POS-System---POSsym
    ```

### 2. Create Your Environment File
    `cp .env.example .env` copies the .env.example file to a .env file that the application will use. All of these live locally at the moment so usernames and passwords are arbitrary.
    
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

Never commit .env to Git! It's already in .gitignore so you shouldn't have to worry about it.

### 3. Start up
`docker compose up --build` will build the docker container on your machine for first run
`docker compose up` will be used every other time you boot up the container

### 4. Confirm everything is running
In a second terminal `docker compose ps` Should show all the services running

### 5. Confirm the API is running
`curl http://localhost:8000/health` should return {status: ok} in your terminal

## Project Structure
```
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
```
### Useful Commands
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

## Workflow!
This will help us stay organized and manage our workflow

##### 1. Pull latest changes from main before you start coding!
`git checkout main` moves you to the main branch
`git pull origin main` pulls the most recent version of the repo to your machine

##### 2. Create a feature branch for the feature you're working on
`git checkout -b feature/branch-name` creates/switches to the feature branch. Any commits you make will go to this branch.

##### 3. Stage your files
These lines allow you to commit all files or a single file respectively
```bash
git add .
git add file-name
```

##### 4. Commit your changes
`git commit -m "your message"` commit your changes with a short/meaningful message

##### 5. Push the changes to the feature branch
`git push -u origin feature/branch-name` pushes new changes to feature branch

##### 6. IMPORTANT! Create a Pull Request to merge to main
After your changes have been made, create a Pull Request via github website. All PRs must be reviewed by at least one person before approved to merge with the main branch.

It is everyone's responsibility to review new changes and stay informed about the overall system. Not every feature may be important to you, but everyone should have a general understanding of what features do. 

I trust everyone understands what constitutes as a major application change vs. a minor bug fix. Please communicate with everyone if changes you make will have major impact on the project. Every major merge should initiate a discussion of some sort to explain changes. Minor bug fixes can be approved/merged via the 1 review PR system.

##### 7. Delete ya branch
After a Pull Request is merged, the feature branch should be deleted both locally and remotely.
```bash
git branch -d feature/branch-name
git push origin --delete feature/branch-name
```
