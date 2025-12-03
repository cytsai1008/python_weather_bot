# Docker Compose Quick Reference

## Files Overview

### `docker-compose.yml` - Default (Development)
- Builds image locally from source
- For development and testing
- Make code changes, rebuild, test

### `docker-compose.prod.yml` - Production
- Uses pre-built image from GHCR
- Includes Watchtower for auto-updates
- No local build needed

## Usage

### Development (Local Build)

```bash
# Build and start
docker-compose up -d

# Rebuild after code changes
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Production (GHCR Image)

**First, update the image name in `docker-compose.prod.yml`:**
```yaml
image: ghcr.io/YOUR_GITHUB_USERNAME/python_weather_bot:latest
```

**Then run:**
```bash
# Start with production config
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop
docker-compose -f docker-compose.prod.yml down
```

### Switch from Local to GHCR (in default compose)

Edit `docker-compose.yml`:

**Comment out:**
```yaml
# build:
#   context: .
#   dockerfile: Dockerfile
```

**Uncomment:**
```yaml
image: ghcr.io/YOUR_USERNAME/python_weather_bot:latest
```

Then:
```bash
docker-compose pull
docker-compose up -d
```

## Features

### Health Checks
Both configs include health monitoring:
```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' taiwan-weather-bot
```

### Resource Limits
- **CPU**: 0.5 cores max, 0.25 cores reserved
- **Memory**: 512MB max, 256MB reserved

Adjust in compose file if needed.

### Log Rotation
- Max 10MB per log file
- Keeps 3 most recent files
- Older logs auto-deleted

### Auto-restart
Service automatically restarts:
- On crash
- After server reboot
- After Docker restart

## Watchtower (Auto-updates)

### In Default Compose
Uncomment the watchtower section:
```yaml
watchtower:
  image: containrrr/watchtower
  # ... rest of config
```

### In Production Compose
Already enabled! Checks for updates every hour.

**Disable auto-update:**
```bash
# Use production compose without watchtower
docker-compose -f docker-compose.prod.yml up -d weather-bot
```

### Manual Update
```bash
# Pull latest image
docker-compose pull

# Restart with new image
docker-compose up -d
```

## Environment Variables

### Using .env file (Recommended)
```env
DISCORD_BOT_TOKEN=xxx
CWA_API_KEY=xxx
GEMINI_API_KEY=xxx
```

### Using environment variables directly
Uncomment in compose file:
```yaml
environment:
  DISCORD_BOT_TOKEN: ${DISCORD_BOT_TOKEN}
  CWA_API_KEY: ${CWA_API_KEY}
  GEMINI_API_KEY: ${GEMINI_API_KEY}
```

Then:
```bash
export DISCORD_BOT_TOKEN=xxx
export CWA_API_KEY=xxx
export GEMINI_API_KEY=xxx
docker-compose up -d
```

## Common Commands

### View Status
```bash
docker-compose ps
```

### View Logs
```bash
# All logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Specific service
docker-compose logs weather-bot
```

### Restart
```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart weather-bot
```

### Update
```bash
# Development (rebuild)
docker-compose build --no-cache
docker-compose up -d

# Production (pull new image)
docker-compose pull
docker-compose up -d
```

### Clean Up
```bash
# Stop and remove containers
docker-compose down

# Also remove volumes
docker-compose down -v

# Also remove images
docker-compose down --rmi all
```

## Monitoring

### Resource Usage
```bash
docker stats taiwan-weather-bot
```

### Container Inspection
```bash
docker inspect taiwan-weather-bot
```

### Health Status
```bash
docker inspect taiwan-weather-bot | grep -A 5 Health
```

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs

# Common issues:
# - Missing .env file
# - Invalid API keys
# - Port conflicts
# - Image pull failures
```

### Out of memory
Increase memory limit in compose file:
```yaml
deploy:
  resources:
    limits:
      memory: 1G
```

### High CPU usage
Lower CPU limit:
```yaml
deploy:
  resources:
    limits:
      cpus: '0.25'
```

### Image pull fails (private GHCR)
```bash
# Login to GHCR
echo $GITHUB_PAT | docker login ghcr.io -u USERNAME --password-stdin

# Then pull
docker-compose pull
```

## Production Checklist

- [ ] `.env` file exists with valid API keys
- [ ] Updated image name in compose file
- [ ] Resource limits appropriate for your server
- [ ] Logging configured properly
- [ ] Health checks enabled
- [ ] Auto-restart enabled
- [ ] Watchtower enabled (optional)
- [ ] Firewall configured if needed

## Best Practices

1. **Development**: Use `docker-compose.yml` (local build)
2. **Production**: Use `docker-compose.prod.yml` (GHCR image)
3. **Keep .env secure**: Never commit to git
4. **Monitor logs**: Check regularly for errors
5. **Set resource limits**: Prevent resource exhaustion
6. **Use version tags**: `v1.0.0` instead of `latest` in production
7. **Enable Watchtower**: Keep bot updated automatically
8. **Backup .env**: Store API keys securely

---

Choose the setup that fits your needs! 🚀
