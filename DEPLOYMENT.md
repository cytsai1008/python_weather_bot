# 🚀 Deployment Guide

Complete guide for deploying the Taiwan Weather Bot using Docker and GitHub Container Registry.

## Quick Deploy from GHCR

### Using Docker Compose (Recommended)

1. Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  weather-bot:
    image: ghcr.io/cytsai1008/python_weather_bot:latest
    container_name: taiwan-weather-bot
    restart: unless-stopped
    env_file:
      - .env
```

2. Create `.env` file with your API keys:

```env
DISCORD_BOT_TOKEN=your_token_here
CWA_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

3. Run:

```bash
docker-compose up -d
```

### Using Docker Run

```bash
docker run -d \
  --name taiwan-weather-bot \
  --restart unless-stopped \
  --env-file .env \
  ghcr.io/cytsai1008/python_weather_bot:latest
```

## GitHub Actions - Automated Builds

### What's Automated

The GitHub Actions workflows automatically:

1. **On Push to Main/Develop:**
   - Builds Docker image
   - Pushes to GHCR with branch name tag
   - Creates `latest` tag for main branch

2. **On Release:**
   - Builds multi-platform images (amd64, arm64)
   - Tags with version number (e.g., `v1.0.0`)
   - Tags with `stable` and `latest`
   - Generates build attestation

3. **On Pull Request:**
   - Builds image to verify it works
   - Does NOT push to registry

### Available Tags

After pushing/releasing, images are available with these tags:

```bash
# Latest stable release
ghcr.io/cytsai1008/python_weather_bot:latest
ghcr.io/cytsai1008/python_weather_bot:stable

# Specific version
ghcr.io/cytsai1008/python_weather_bot:v1.0.0
ghcr.io/cytsai1008/python_weather_bot:1.0
ghcr.io/cytsai1008/python_weather_bot:1

# Branch builds
ghcr.io/cytsai1008/python_weather_bot:main
ghcr.io/cytsai1008/python_weather_bot:develop
```

## Setup GitHub Actions

### 1. Enable GitHub Container Registry

GitHub Container Registry (GHCR) is enabled by default, but you need to:

1. Go to your repository
2. Settings → Actions → General
3. Scroll to "Workflow permissions"
4. Select **"Read and write permissions"**
5. Check **"Allow GitHub Actions to create and approve pull requests"**
6. Save

### 2. Make Package Public (Optional)

After first build:

1. Go to your GitHub profile → Packages
2. Find `python_weather_bot`
3. Package Settings → Change visibility to **Public**

Or keep it private and use with authentication.

## Creating a Release

To trigger the release workflow:

```bash
# Tag a new version
git tag v1.0.0
git push origin v1.0.0
```

Or use GitHub UI:
1. Go to repository → Releases
2. Click "Create a new release"
3. Choose a tag (e.g., `v1.0.0`)
4. Fill in release notes
5. Publish release

GitHub Actions will automatically build and push the image.

## Pulling Images

### Public Images

```bash
docker pull ghcr.io/cytsai1008/python_weather_bot:latest
```

### Private Images

```bash
# Create a Personal Access Token (PAT)
# Settings → Developer settings → Personal access tokens → Tokens (classic)
# Select scopes: read:packages

# Login to GHCR
echo $GITHUB_PAT | docker login ghcr.io -u USERNAME --password-stdin

# Pull image
docker pull ghcr.io/cytsai1008/python_weather_bot:latest
```

## Deployment Platforms

### 1. VPS (Ubuntu/Debian)

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Create directory
mkdir ~/weather-bot
cd ~/weather-bot

# Create .env file
nano .env
# (Add your API keys)

# Create docker-compose.yml
nano docker-compose.yml
# (Copy the compose file from above)

# Pull and run
docker-compose up -d

# Check logs
docker-compose logs -f
```

### 2. Railway

1. Go to [Railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Select your repository
4. Add environment variables:
   - `DISCORD_BOT_TOKEN`
   - `CWA_API_KEY`
   - `GEMINI_API_KEY`
5. Deploy!

Railway will automatically use your Dockerfile.

### 3. Fly.io

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Login: `fly auth login`
3. Create `fly.toml`:

```toml
app = "taiwan-weather-bot"

[build]
  image = "ghcr.io/cytsai1008/python_weather_bot:latest"

[[services]]
  internal_port = 8080
  protocol = "tcp"
```

4. Set secrets:
```bash
fly secrets set DISCORD_BOT_TOKEN=xxx
fly secrets set CWA_API_KEY=xxx
fly secrets set GEMINI_API_KEY=xxx
```

5. Deploy: `fly deploy`

### 4. Oracle Cloud (Free Tier)

Oracle offers free ARM64 instances:

```bash
# SSH to instance
ssh ubuntu@your-instance-ip

# Install Docker (ARM64)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Pull ARM64 image
docker pull ghcr.io/cytsai1008/python_weather_bot:latest

# Run with .env file
docker run -d \
  --name weather-bot \
  --restart unless-stopped \
  --env-file .env \
  ghcr.io/cytsai1008/python_weather_bot:latest
```

### 5. Raspberry Pi

Works great on ARM64 Raspberry Pi:

```bash
# Same as VPS deployment
docker pull ghcr.io/cytsai1008/python_weather_bot:latest
docker-compose up -d
```

## Multi-Platform Support

The GitHub Actions workflow builds for:
- **linux/amd64** (x86_64) - Most servers, VPS
- **linux/arm64** (ARM64) - Raspberry Pi, Oracle ARM, Apple Silicon

Docker automatically pulls the correct architecture.

## Monitoring

### View Logs

```bash
# Docker Compose
docker-compose logs -f

# Docker
docker logs -f taiwan-weather-bot
```

### Check Status

```bash
# Docker Compose
docker-compose ps

# Docker
docker ps | grep weather-bot
```

### Resource Usage

```bash
docker stats taiwan-weather-bot
```

## Updating

### Auto-update (Watchtower)

Add to your `docker-compose.yml`:

```yaml
services:
  weather-bot:
    image: ghcr.io/cytsai1008/python_weather_bot:latest
    # ... other config

  watchtower:
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: --interval 300 taiwan-weather-bot
```

Watchtower checks for updates every 5 minutes.

### Manual Update

```bash
# Pull latest image
docker-compose pull

# Restart with new image
docker-compose up -d

# Or in one command
docker-compose pull && docker-compose up -d
```

## Troubleshooting

### Image Pull Fails (Private)

```bash
# Create GitHub PAT with read:packages
# Login to GHCR
echo $PAT | docker login ghcr.io -u USERNAME --password-stdin
```

### Bot Won't Start

```bash
# Check logs
docker-compose logs

# Common issues:
# 1. Missing .env file
# 2. Invalid API keys
# 3. Wrong image architecture
```

### Check Image Details

```bash
# Inspect image
docker image inspect ghcr.io/cytsai1008/python_weather_bot:latest

# Check platforms
docker manifest inspect ghcr.io/cytsai1008/python_weather_bot:latest
```

## CI/CD Workflow Details

### Build Process

```
Push to main → Trigger Workflow → Build Image → Run Tests → Push to GHCR → Tag as latest
```

### Caching

GitHub Actions uses layer caching to speed up builds:
- First build: ~2-3 minutes
- Subsequent builds: ~30-60 seconds

### Security

- Images are signed with build attestation
- Runs as non-root user
- Minimal attack surface (slim base image)
- Automated dependency updates possible with Dependabot

## Cost

- **GitHub Actions**: 2000 minutes/month free (private repos)
- **GHCR Storage**: 500MB free, then $0.25/GB/month
- **Bandwidth**: Unlimited for public images

This bot uses ~150MB storage = **FREE** ✅

## Best Practices

1. **Use version tags in production**: `v1.0.0` instead of `latest`
2. **Enable auto-restart**: `restart: unless-stopped`
3. **Set resource limits**: Prevent resource exhaustion
4. **Monitor logs**: Use logging drivers
5. **Keep secrets secure**: Never commit `.env` to git
6. **Regular updates**: Pull new images weekly

---

Your bot is now deployable anywhere Docker runs! 🎉
