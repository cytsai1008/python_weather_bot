# 🐳 Docker Deployment Guide

Quick guide to run the Taiwan Weather Bot using Docker.

## Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (included with Docker Desktop)
- API keys configured in `.env` file

## Quick Start

### 1. Setup Environment Variables

Make sure your `.env` file exists with all API keys:

```bash
# Should already exist, if not:
cp .env.example .env
# Edit .env and add your keys
```

### 2. Build and Run

```bash
# Build and start the bot
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down
```

That's it! Your bot is now running in Docker.

## Docker Commands Reference

### Build & Run

```bash
# Build the image
docker-compose build

# Start the bot (detached mode)
docker-compose up -d

# Start with build (if you made code changes)
docker-compose up -d --build

# Start and view logs
docker-compose up
```

### Monitoring

```bash
# View logs
docker-compose logs

# Follow logs (real-time)
docker-compose logs -f

# View last 100 lines
docker-compose logs --tail=100

# Check container status
docker-compose ps
```

### Stopping & Cleanup

```bash
# Stop the bot
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop and remove images
docker-compose down --rmi all
```

### Restart

```bash
# Restart the bot
docker-compose restart

# Restart with new code
docker-compose down
docker-compose up -d --build
```

## Manual Docker Commands

If you prefer using Docker directly without compose:

```bash
# Build image
docker build -t taiwan-weather-bot .

# Run container
docker run -d \
  --name weather-bot \
  --env-file .env \
  --restart unless-stopped \
  taiwan-weather-bot

# View logs
docker logs -f weather-bot

# Stop and remove
docker stop weather-bot
docker rm weather-bot
```

## Dockerfile Explained

```dockerfile
# Multi-stage build
FROM python:3.11-slim as builder  # Build dependencies
FROM python:3.11-slim             # Final minimal image

# Key features:
- Multi-stage build (smaller final image)
- Non-root user (security)
- Minimal Python slim image (~50MB base)
- Health check included
- Optimized layer caching
```

## Environment Variables

The bot requires these environment variables (from `.env`):

- `DISCORD_BOT_TOKEN` - Your Discord bot token
- `CWA_API_KEY` - Taiwan CWA API key
- `GEMINI_API_KEY` - Google Gemini API key

Docker Compose automatically loads from `.env` file.

## Resource Limits

Default limits in `docker-compose.yml`:

- **CPU**: 0.5 cores max, 0.25 cores reserved
- **Memory**: 512MB max, 256MB reserved

Adjust in `docker-compose.yml` if needed:

```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'      # Increase if needed
      memory: 1G
```

## Troubleshooting

### Bot not starting

```bash
# Check logs for errors
docker-compose logs

# Common issues:
# 1. Missing .env file
# 2. Invalid API keys
# 3. Network issues
```

### Check if container is running

```bash
docker-compose ps

# Should show:
# NAME                  STATUS
# taiwan-weather-bot    Up X minutes
```

### Restart with fresh build

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### View real-time resource usage

```bash
docker stats taiwan-weather-bot
```

### Access container shell

```bash
docker-compose exec weather-bot /bin/sh
```

## Production Deployment

### Using Docker Hub

```bash
# Tag your image
docker tag taiwan-weather-bot yourusername/taiwan-weather-bot:latest

# Push to Docker Hub
docker push yourusername/taiwan-weather-bot:latest

# Pull and run on server
docker pull yourusername/taiwan-weather-bot:latest
docker-compose up -d
```

### Using a VPS

1. Install Docker on VPS
2. Copy files to server:
   ```bash
   scp -r ./* user@server:/app/weather-bot/
   ```
3. SSH into server and run:
   ```bash
   cd /app/weather-bot
   docker-compose up -d
   ```

### Auto-restart on Server Reboot

The `restart: unless-stopped` policy ensures the bot automatically restarts if:
- Server reboots
- Container crashes
- Docker daemon restarts

## Security Notes

- ✅ Runs as non-root user (`botuser`)
- ✅ `.env` file excluded from image (`.dockerignore`)
- ✅ Minimal base image (fewer vulnerabilities)
- ✅ No unnecessary packages installed
- ⚠️ Keep `.env` file secure (never commit to git)

## Updating the Bot

When you make code changes:

```bash
# Method 1: Rebuild and restart
docker-compose down
docker-compose up -d --build

# Method 2: Rolling update (no downtime)
docker-compose up -d --build
```

## Alternative: Pure Distroless (Advanced)

For an even smaller image using Google's distroless:

```dockerfile
FROM gcr.io/distroless/python3-debian11

COPY --from=builder /root/.local /root/.local
COPY *.py /app/

WORKDIR /app
ENV PATH=/root/.local/bin:$PATH

CMD ["bot.py"]
```

⚠️ Note: Distroless images have no shell, making debugging harder.

## Logs Management

Logs are automatically rotated:
- Max size per file: 10MB
- Keep 3 most recent files
- Older logs auto-deleted

Change in `docker-compose.yml`:

```yaml
logging:
  options:
    max-size: "50m"  # Increase size
    max-file: "5"    # Keep more files
```

## Performance Tips

1. **Build cache**: Don't change requirements.txt unnecessarily
2. **Layer optimization**: Most-changed files last in Dockerfile
3. **Multi-stage builds**: Keeps final image small
4. **Resource limits**: Prevents bot from consuming too much

## Health Checks

The container includes a health check:
- Runs every 30 seconds
- If 3 consecutive failures, container marked unhealthy
- Can trigger auto-restart with orchestration tools

Check health:
```bash
docker inspect --format='{{.State.Health.Status}}' taiwan-weather-bot
```

---

Your bot is now containerized and ready for deployment anywhere Docker runs! 🚀
