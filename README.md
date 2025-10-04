# LEMP Containers (Frontend + Backend + MySQL) with /api/time

This project follows the provided workflow: Nginx frontend (proxies /api), Flask+Gunicorn backend, MySQL database. The required `/api/time` endpoint returns MySQL server time (`SELECT NOW()`), and the frontend displays it.

## Local Dev
1) Copy `.env.example` to `.env` and edit secrets
2) Start:
   ```bash
   docker compose -f docker-compose.dev.yml --env-file .env up --build -d
   ```
3) Open http://localhost:8080 (frontend)
4) Test API:
   ```bash
   curl http://localhost:8080/api/time
   ```

## Build & Push Images
```bash
# login first
docker login

# Backend
docker build -f backend/Dockerfile -t ${DOCKERHUB_USERNAME}/lemp-backend:1.0.0 .
docker tag ${DOCKERHUB_USERNAME}/lemp-backend:1.0.0 ${DOCKERHUB_USERNAME}/lemp-backend:latest
docker push ${DOCKERHUB_USERNAME}/lemp-backend:1.0.0
docker push ${DOCKERHUB_USERNAME}/lemp-backend:latest

# Frontend
docker build -f frontend/Dockerfile -t ${DOCKERHUB_USERNAME}/lemp-frontend:1.0.0 .
docker tag ${DOCKERHUB_USERNAME}/lemp-frontend:1.0.0 ${DOCKERHUB_USERNAME}/lemp-frontend:latest
docker push ${DOCKERHUB_USERNAME}/lemp-frontend:1.0.0
docker push ${DOCKERHUB_USERNAME}/lemp-frontend:latest
```

## Deploy on Linux VM
1) Install Docker & Compose plugin, then set up `/opt/lemp`
2) Copy `.env` and `docker-compose.prod.yml` to the VM
3) Run:
```bash
cd /opt/lemp
docker compose --env-file .env pull
docker compose --env-file .env up -d
```
Open `http://VM_IP/`

## Files
- `backend/app.py` – Flask app with `/api/time`
- `frontend/index.html` + `frontend/nginx.conf` – Nginx static & proxy
- `db/init/init.sql` – DB/user bootstrap
- `docker-compose.dev.yml` – local builds
- `docker-compose.prod.yml` – pulls from Docker Hub
```

