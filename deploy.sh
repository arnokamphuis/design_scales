#!/bin/bash

# Terrain Scaling Calculator - Docker Deployment Script

echo "🐳 Terrain Scaling Calculator - Docker Deployment"
echo "=================================================="

# Check if Docker/Podman is available
if command -v podman &> /dev/null; then
    CONTAINER_CMD="podman"
    COMPOSE_CMD="podman-compose"
    echo "✅ Using Podman"
elif command -v docker &> /dev/null; then
    CONTAINER_CMD="docker"
    COMPOSE_CMD="docker-compose"
    echo "✅ Using Docker"
else
    echo "❌ Neither Docker nor Podman found. Please install one of them."
    exit 1
fi

# Function to build and run
deploy() {
    echo ""
    echo "🔨 Building container image..."
    $CONTAINER_CMD build -t terrain-scaling-calculator .
    
    if [ $? -eq 0 ]; then
        echo "✅ Build completed successfully!"
        echo ""
        echo "🚀 Starting container on port 4375..."
        
        # Stop any existing container
        $CONTAINER_CMD stop terrain-scaling-calculator 2>/dev/null || true
        $CONTAINER_CMD rm terrain-scaling-calculator 2>/dev/null || true
        
        # Run the container
        $CONTAINER_CMD run -d \
            --name terrain-scaling-calculator \
            -p 4375:80 \
            --restart unless-stopped \
            terrain-scaling-calculator
        
        if [ $? -eq 0 ]; then
            echo "✅ Container started successfully!"
            echo ""
            echo "🌐 Application is now available at:"
            echo "   http://localhost:4375"
            echo ""
            echo "📊 Container status:"
            $CONTAINER_CMD ps | grep terrain-scaling-calculator
            echo ""
            echo "📝 To stop the application:"
            echo "   $CONTAINER_CMD stop terrain-scaling-calculator"
            echo ""
            echo "📝 To view logs:"
            echo "   $CONTAINER_CMD logs terrain-scaling-calculator"
        else
            echo "❌ Failed to start container"
            exit 1
        fi
    else
        echo "❌ Build failed"
        exit 1
    fi
}

# Function to stop
stop() {
    echo ""
    echo "🛑 Stopping terrain scaling calculator..."
    $CONTAINER_CMD stop terrain-scaling-calculator
    $CONTAINER_CMD rm terrain-scaling-calculator
    echo "✅ Application stopped and container removed"
}

# Function to show logs
logs() {
    echo ""
    echo "📝 Container logs:"
    $CONTAINER_CMD logs -f terrain-scaling-calculator
}

# Function to show status
status() {
    echo ""
    echo "📊 Container status:"
    $CONTAINER_CMD ps -a | grep terrain-scaling-calculator
    echo ""
    echo "🌐 If running, application should be available at:"
    echo "   http://localhost:4375"
}

# Parse command line arguments
case "$1" in
    "deploy" | "start" | "")
        deploy
        ;;
    "stop")
        stop
        ;;
    "logs")
        logs
        ;;
    "status")
        status
        ;;
    "restart")
        stop
        sleep 2
        deploy
        ;;
    *)
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  deploy|start  Build and start the application (default)"
        echo "  stop          Stop and remove the container"
        echo "  restart       Stop and restart the application"
        echo "  logs          Show container logs"
        echo "  status        Show container status"
        echo ""
        exit 1
        ;;
esac