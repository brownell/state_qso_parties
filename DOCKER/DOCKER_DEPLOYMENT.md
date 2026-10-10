# Texas QSO Party - Docker Deployment Guide

This guide covers deploying the TXQP web application using Docker.

## 🐳 What Docker Handles

### Persistent Data (Survives Container Restarts)
- ✅ **SQLite Database** → Volume: `txqp-database`
- ✅ **Uploaded Logs** → Volume: `txqp-logs`
- ✅ **HTML Results** → Volume: `txqp-results`
- ✅ **Data Files** (parishes, states) → Mounted from host

### Temporary Data (Cleared on Restart)
- ✅ **Temp Files** → Volume: `txqp-temp` (ephemeral)
- ✅ **Application Cache** → Inside container

## 📁 Directory Structure

```
your-project/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env                     # Create from .env.example
├── app.py
├── processor.py
├── html_results.py
├── requirements.txt
├── templates/
│   ├── upload.html
│   └── results.html
├── static/
│   ├── css/
│   └── js/
├── data/                    # MUST EXIST with data files
│   ├── LA_Parish_Abbrevs.txt
│   └── WVE_Abbrevs.txt
└── config/                  # Your config files
    └── config.py
```

## 🚀 Quick Start

### 1. Prerequisites

- Docker installed
- Docker Compose installed
- Data files present in `data/` directory

### 2. Setup Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit with your values (CHANGE SECRET_KEY!)
nano .env
```

**Important:** Change the `SECRET_KEY` in `.env`:
```bash
SECRET_KEY=your-random-secret-key-here-make-it-long-and-random
```

### 3. Ensure Data Files Exist

Create the data files if they don't exist:

```bash
mkdir -p data

# Create LA_Parish_Abbrevs.txt with all 64 parishes
cat > data/LA_Parish_Abbrevs.txt << 'EOF'
ACA
ALL
ASC
...
EOF

# Create WVE_Abbrevs.txt with states and provinces
cat > data/WVE_Abbrevs.txt << 'EOF'
AL
AK
AZ
...
EOF
```

### 4. Build and Run

```bash
# Build and start in detached mode
docker-compose up -d --build

# Check logs
docker-compose logs -f

# Check status
docker-compose ps
```

### 5. Access Application

Open browser to: **http://localhost:5000**

- Log Upload: http://localhost:5000/
- Results Lookup: http://localhost:5000/results
- Health Check: http://localhost:5000/health

## 🔧 Docker Commands

### Start/Stop

```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# Restart containers
docker-compose restart

# Stop and remove volumes (⚠️ DELETES DATA!)
docker-compose down -v
```

### Logs

```bash
# View logs (follow mode)
docker-compose logs -f

# View logs (last 100 lines)
docker-compose logs --tail=100

# View logs for specific service
docker-compose logs -f txqp-web
```

### Rebuild

```bash
# Rebuild after code changes
docker-compose up -d --build

# Force rebuild (no cache)
docker-compose build --no-cache
docker-compose up -d
```

### Access Container

```bash
# Open shell in running container
docker-compose exec txqp-web bash

# Run Python in container
docker-compose exec txqp-web python

# Run one-off command
docker-compose exec txqp-web ls -la /app/database
```

## 💾 Data Persistence

### Volumes

Docker creates named volumes for persistent data:

```bash
# List volumes
docker volume ls | grep txqp

# Inspect volume
docker volume inspect txqp-database

# Backup volume
docker run --rm -v txqp-database:/data -v $(pwd):/backup \
  alpine tar czf /backup/txqp-database-backup.tar.gz -C /data .

# Restore volume
docker run --rm -v txqp-database:/data -v $(pwd):/backup \
  alpine tar xzf /backup/txqp-database-backup.tar.gz -C /data
```

### Database Location

Inside container: `/app/database/txqp.db`

To access from host:
```bash
# Copy database out
docker cp txqp-web:/app/database/txqp.db ./txqp.db

# Copy database in
docker cp ./txqp.db txqp-web:/app/database/txqp.db
```

### HTML Results Location

Inside container: `/app/HTML_RESULTS/`

To add pre-generated results:
```bash
# Copy results into container
docker cp HTML_RESULTS/2026/ txqp-web:/app/HTML_RESULTS/
```

## 🔐 Security

### Change Secret Key

**Before deploying to production**, change the secret key:

```bash
# Generate a random secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Add to .env file
SECRET_KEY=<generated-key-here>
```

### Run as Non-Root

The container runs as user `txqp` (UID 1000), not root.

### File Permissions

If you have permission issues with volumes:

```bash
# Check volume ownership
docker-compose exec txqp-web ls -la /app/database

# Fix ownership (if needed)
docker-compose exec --user root txqp-web chown -R txqp:txqp /app/database
```

## 🌐 Production Deployment

### Using Nginx Reverse Proxy

Create `nginx.conf`:

```nginx
server {
    listen 80;
    server_name txqp.example.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        proxy_pass http://localhost:5000/static;
    }

    client_max_body_size 10M;
}
```

### SSL with Let's Encrypt

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d txqp.example.com

# Auto-renewal is configured automatically
```

### Update docker-compose.yml for Production

```yaml
services:
  txqp-web:
    # ... existing config ...
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}  # From .env file
    restart: always  # Changed from unless-stopped
```

## 📊 Monitoring

### Health Check

```bash
# Check container health
docker-compose ps

# Manual health check
curl http://localhost:5000/health
```

### Resource Usage

```bash
# View resource usage
docker stats txqp-web

# View disk usage
docker system df
```

## 🔄 Updates and Maintenance

### Update Application Code

```bash
# 1. Pull latest code
git pull

# 2. Rebuild and restart
docker-compose up -d --build

# 3. Check logs
docker-compose logs -f
```

### Update Dependencies

```bash
# Edit requirements.txt
# Then rebuild
docker-compose build --no-cache
docker-compose up -d
```

### Database Migrations

If you need to run database migrations:

```bash
# Access container
docker-compose exec txqp-web bash

# Run migration script
python migrate.py

# Or directly
docker-compose exec txqp-web python migrate.py
```

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs txqp-web

# Check if port 5000 is in use
lsof -i :5000

# Try running without detached mode (see errors)
docker-compose up
```

### Database Locked

```bash
# If SQLite database is locked
docker-compose restart
```

### Permission Denied

```bash
# Fix volume permissions
docker-compose down
docker-compose up -d
docker-compose exec --user root txqp-web chown -R txqp:txqp /app
```

### Can't Access from Outside

```bash
# Check firewall
sudo ufw status
sudo ufw allow 5000

# Check if container is running
docker-compose ps

# Check port mapping
docker port txqp-web
```

### Data Files Not Found

```bash
# Verify data files are mounted
docker-compose exec txqp-web ls -la /app/data/

# If missing, check docker-compose.yml volumes section
# Make sure ./data exists on host
```

## 📦 Backup and Restore

### Full Backup

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/$DATE"

mkdir -p $BACKUP_DIR

# Backup database
docker run --rm -v txqp-database:/data -v $(pwd)/$BACKUP_DIR:/backup \
  alpine tar czf /backup/database.tar.gz -C /data .

# Backup logs
docker run --rm -v txqp-logs:/data -v $(pwd)/$BACKUP_DIR:/backup \
  alpine tar czf /backup/logs.tar.gz -C /data .

# Backup results
docker run --rm -v txqp-results:/data -v $(pwd)/$BACKUP_DIR:/backup \
  alpine tar czf /backup/results.tar.gz -C /data .

echo "Backup complete: $BACKUP_DIR"
```

### Restore from Backup

```bash
#!/bin/bash
# restore.sh

BACKUP_DIR=$1

# Restore database
docker run --rm -v txqp-database:/data -v $(pwd)/$BACKUP_DIR:/backup \
  alpine tar xzf /backup/database.tar.gz -C /data

# Restore logs
docker run --rm -v txqp-logs:/data -v $(pwd)/$BACKUP_DIR:/backup \
  alpine tar xzf /backup/logs.tar.gz -C /data

# Restore results
docker run --rm -v txqp-results:/data -v $(pwd)/$BACKUP_DIR:/backup \
  alpine tar xzf /backup/results.tar.gz -C /data

echo "Restore complete from: $BACKUP_DIR"
```

## 🎯 Development vs Production

### Development

```yaml
# docker-compose.dev.yml
services:
  txqp-web:
    build: .
    volumes:
      # Mount code for live reload
      - ./app.py:/app/app.py
      - ./processor.py:/app/processor.py
      - ./templates:/app/templates
      - ./static:/app/static
    environment:
      - FLASK_ENV=development
      - FLASK_DEBUG=1
    command: flask run --host=0.0.0.0 --port=5000
```

Run with:
```bash
docker-compose -f docker-compose.dev.yml up
```

### Production

Use the standard `docker-compose.yml` with:
- Gunicorn (multiple workers)
- Production environment
- Auto-restart enabled
- Health checks

## 📝 Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | (required) | Flask secret key |
| `CONTEST_YEAR` | 2026 | Current contest year |
| `DATABASE_PATH` | /app/database/txqp.db | SQLite database path |
| `UPLOAD_FOLDER` | /app/logs/incoming | Upload directory |
| `HTML_RESULTS_DIR` | /app/HTML_RESULTS | Results output directory |
| `TEMP_DIR` | /app/temp | Temporary files directory |
| `WORKERS` | 4 | Gunicorn worker processes |
| `TIMEOUT` | 120 | Gunicorn timeout (seconds) |

## ✅ Pre-Deployment Checklist

- [ ] Change SECRET_KEY in .env
- [ ] Data files exist (LA_Parish_Abbrevs.txt, WVE_Abbrevs.txt)
- [ ] Tested locally with docker-compose
- [ ] Set up backup schedule
- [ ] Configure SSL/HTTPS
- [ ] Set up monitoring/logging
- [ ] Configure firewall rules
- [ ] Test database persistence
- [ ] Test volume backups/restores

## 🆘 Getting Help

If you encounter issues:

1. Check logs: `docker-compose logs -f`
2. Verify volumes: `docker volume ls | grep txqp`
3. Check container status: `docker-compose ps`
4. Access container: `docker-compose exec txqp-web bash`
5. Review this guide's troubleshooting section

---

**Ready to deploy!** 🚀

Start with: `docker-compose up -d --build`
