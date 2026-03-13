# ─────────────────────────────────────────────────────────────────────────────
# HFT Practice — API Gateway Dockerfile
# Mirrors the production HFT Django service Dockerfiles
#
# Key production fixes applied here:
#   ✅ No redis-server inside container — uses ElastiCache
#   ✅ No migrations on startup — run separately via CodePipeline
#   ✅ No makemigrations — never in production containers
#   ✅ Gunicorn binds to 0.0.0.0:8000
#   ✅ stdout logging — captured by ECS → CloudWatch automatically
# ─────────────────────────────────────────────────────────────────────────────

FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user for security
RUN addgroup --system appgroup && adduser --system --group appuser
USER appuser

# Expose port 8000 (matches ALB target group and ECS task definition)
EXPOSE 8000

# Health check — ALB uses this to verify container is running
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Start Gunicorn — production WSGI server
# Workers = 2*CPU+1 formula, but capped at 2 for practice (256 CPU Fargate)
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "api_gateway.wsgi:application"]
