# ─────────────────────────────────────────────────────────────────────────────
# HFT Practice — Frontend Dockerfile
# Uses nginx to serve the static HTML dashboard on port 80
# Mirrors the production HFT-Frontend ECS service
# ─────────────────────────────────────────────────────────────────────────────

FROM nginx:1.25-alpine

# Remove default nginx page
RUN rm -rf /usr/share/nginx/html/*

# Copy our dashboard
COPY index.html /usr/share/nginx/html/index.html

# Custom nginx config — proxy /api/* to api-gateway service
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -qO- http://localhost:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
