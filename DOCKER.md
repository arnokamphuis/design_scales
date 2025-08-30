# Docker Deployment Guide

This guide explains how to run the Terrain Scaling Calculator using Docker or Podman.

## 🚀 Quick Start

### Using the Deploy Script (Recommended)
```bash
# Make the script executable
chmod +x deploy.sh

# Deploy the application
./deploy.sh

# The application will be available at http://localhost:4375
```

### Manual Deployment

#### Option 1: Docker
```bash
# Build the image
docker build -t terrain-scaling-calculator .

# Run the container
docker run -d \
  --name terrain-scaling-calculator \
  -p 4375:80 \
  --restart unless-stopped \
  terrain-scaling-calculator

# Access at http://localhost:4375
```

#### Option 2: Podman
```bash
# Build the image
podman build -t terrain-scaling-calculator .

# Run the container
podman run -d \
  --name terrain-scaling-calculator \
  -p 4375:80 \
  --restart unless-stopped \
  terrain-scaling-calculator

# Access at http://localhost:4375
```

#### Option 3: Docker Compose
```bash
# Start with Docker Compose
docker-compose up -d

# Stop with Docker Compose
docker-compose down
```

## 📋 Available Commands

### Deploy Script Commands
```bash
./deploy.sh deploy    # Build and start (default)
./deploy.sh stop      # Stop and remove container
./deploy.sh restart   # Restart the application
./deploy.sh logs      # Show container logs
./deploy.sh status    # Show container status
```

### Manual Container Management
```bash
# Check container status
docker ps | grep terrain-scaling-calculator

# View logs
docker logs terrain-scaling-calculator

# Stop container
docker stop terrain-scaling-calculator

# Remove container
docker rm terrain-scaling-calculator

# Remove image
docker rmi terrain-scaling-calculator
```

## 🔧 Configuration

### Port Configuration
By default, the application runs on port **4375**. To change the port:

```bash
# Using custom port (e.g., 8080)
docker run -d --name terrain-scaling-calculator -p 8080:80 terrain-scaling-calculator
```

### Environment Variables
The application is a static web app and doesn't require environment variables.

### Volumes
No persistent volumes are needed as this is a stateless application.

## 🏗️ Build Details

### Image Details
- **Base Image**: `nginx:alpine`
- **Size**: ~25MB (compressed)
- **Architecture**: Multi-architecture (x86_64, arm64)

### What's Included
- Modern web application (HTML, CSS, JavaScript)
- Nginx web server with optimized configuration
- Security headers and gzip compression
- Static asset caching

### Build Process
1. Starts with nginx:alpine base image
2. Removes default nginx content
3. Copies webapp files to nginx html directory
4. Applies custom nginx configuration
5. Exposes port 80
6. Sets nginx as the entry point

## 🌐 Access Information

Once running, access the application at:
- **Local**: http://localhost:4375
- **Network**: http://[your-ip]:4375

## 🛠️ Troubleshooting

### Container Won't Start
```bash
# Check logs
docker logs terrain-scaling-calculator

# Check if port is already in use
netstat -an | grep 4375
```

### Port Already in Use
```bash
# Use a different port
docker run -d --name terrain-scaling-calculator -p 8080:80 terrain-scaling-calculator
```

### Permission Issues (Linux)
```bash
# Make deploy script executable
chmod +x deploy.sh
```

### Container Health Check
```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' terrain-scaling-calculator
```

## 🔄 Updates

To update the application:
```bash
# Stop and remove old container
./deploy.sh stop

# Rebuild with latest changes
./deploy.sh deploy
```

## 📊 Performance

### Resource Usage
- **Memory**: ~10MB
- **CPU**: Minimal (only serves static files)
- **Disk**: ~25MB

### Scalability
For high traffic, consider:
- Using a reverse proxy (nginx, traefik)
- Running multiple instances behind a load balancer
- Enabling nginx caching for static assets

## 🔐 Security

The nginx configuration includes:
- Security headers (X-Frame-Options, X-Content-Type-Options, etc.)
- Gzip compression
- Static asset caching
- No directory browsing

## 📝 Notes

- This is a **stateless application** - no data persistence needed
- All calculations are performed **client-side** (in the browser)
- The container only serves static files
- No backend APIs or databases required