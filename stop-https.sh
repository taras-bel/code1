#!/bin/bash

# NoaMetrics HTTPS Stop Script for Ubuntu
# This script stops the application

set -e  # Exit on any error

echo "🛑 Stopping NoaMetrics..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed."
    exit 1
fi

# Check if the docker-compose.https.yml file exists
if [ ! -f "docker-compose.https.yml" ]; then
    print_error "docker-compose.https.yml not found. Are you in the correct directory?"
    exit 1
fi

# Stop the services
print_status "Stopping NoaMetrics services..."
docker-compose -f docker-compose.https.yml down

# Remove containers
print_status "Removing containers..."
docker-compose -f docker-compose.https.yml rm -f

# Optional: Remove images (uncomment if you want to remove images too)
# print_status "Removing images..."
# docker-compose -f docker-compose.https.yml down --rmi all

# Optional: Remove volumes (uncomment if you want to remove volumes too)
# print_status "Removing volumes..."
# docker-compose -f docker-compose.https.yml down -v

# Check if any containers are still running
if docker-compose -f docker-compose.https.yml ps | grep -q "Up"; then
    print_warning "Some containers are still running. Force stopping..."
    docker-compose -f docker-compose.https.yml down --remove-orphans
fi

# Clean up any dangling containers
print_status "Cleaning up dangling containers..."
docker container prune -f 2>/dev/null || true

# Clean up any dangling networks
print_status "Cleaning up dangling networks..."
docker network prune -f 2>/dev/null || true

# Display cleanup information
echo ""
echo "🧹 Cleanup completed!"
echo ""
echo "📊 Docker system info:"
echo "   Containers: $(docker ps -q | wc -l | tr -d ' ') running"
echo "   Images:     $(docker images -q | wc -l | tr -d ' ') total"
echo "   Networks:   $(docker network ls -q | wc -l | tr -d ' ') total"
echo ""
echo "🔧 To start again:"
echo "   ./start-https.sh"
echo ""
echo "🗑️  To completely clean up (removes all unused Docker resources):"
echo "   docker system prune -a"
echo ""

print_success "NoaMetrics stopped successfully!" 