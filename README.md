# HFT Practice Application

Sample application that mirrors the HFT production architecture.
Used for practicing AWS + Terraform deployments.

## Repository Structure

```
hft-practice-app/
├── api-gateway/        ← Django REST API (port 8000)
│   ├── apps/
│   │   ├── health/     ← Health check endpoints (used by ALB)
│   │   ├── trades/     ← Trade order CRUD + Celery tasks
│   │   └── users/      ← Service info endpoint
│   ├── api_gateway/    ← Django settings, urls, wsgi
│   ├── Dockerfile      ← Builds the ECS container image
│   ├── buildspec.yml   ← CodeBuild instructions
│   └── requirements.txt
│
└── frontend/           ← Nginx + HTML dashboard (port 80)
    ├── index.html      ← Trading dashboard UI
    ├── nginx.conf      ← Nginx proxy config
    ├── Dockerfile
    └── buildspec.yml
```

## Services Relationship

```
Browser → CloudFront → ALB → frontend (nginx, port 80)
                           → api-gateway (Django, port 8000)
                                      → ElastiCache Redis (Celery broker)
                                      → RDS PostgreSQL (database)
```

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET    | /              | Health check (used by ALB) |
| GET    | /health/       | Health check |
| GET    | /ready/        | Readiness check (tests DB connection) |
| GET    | /api/trades/   | List all trades |
| POST   | /api/trades/   | Create a new trade order |
| GET    | /api/trades/{id}/ | Get a specific trade |
| POST   | /api/trades/{id}/execute/ | Execute a pending trade |
| GET    | /api/trades/summary/ | Trade summary by status |
| GET    | /api/users/info/ | Service information |

## Local Development (without Docker)

```bash
cd api-gateway
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Then open: http://localhost:8000/

## Local Development (with Docker)

```bash
cd api-gateway
docker build -t hft-api-gateway .
docker run -p 8000:8000 hft-api-gateway
```

## How CodePipeline Uses This Repo

1. You push code to GitHub main branch
2. CodePipeline detects the push via the GitHub connection
3. CodeBuild runs `buildspec.yml` — builds Docker image, pushes to ECR
4. CodePipeline deploys the new image to ECS using `imagedefinitions.json`
5. ECS does a rolling deployment (old tasks stay up until new ones are healthy)

## Environment Variables Injected by ECS

| Variable | Source | Purpose |
|----------|--------|---------|
| DATABASE_URL | Secrets Manager | PostgreSQL connection string |
| SECRET_KEY | Secrets Manager | Django secret key |
| CELERY_BROKER_URL | ECS task definition | Redis endpoint |
| CELERY_RESULT_BACKEND | ECS task definition | Redis endpoint |
| ENVIRONMENT_TYPE | ECS task definition | practice / production |
 
