#!/bin/bash

# NoaMetrics HTTPS Startup Script for Ubuntu
# This script starts the application with HTTPS support

set -e  # Exit on any error

echo "🚀 Starting NoaMetrics with HTTPS..."

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

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_status "Checking Docker and Docker Compose installation..."
docker --version
docker-compose --version
print_success "Docker and Docker Compose are available"

# Create ssl directory if it doesn't exist
if [ ! -d "ssl" ]; then
    print_status "Creating ssl directory..."
    mkdir -p ssl
fi

# Check if SSL certificates exist
if [ ! -f "ssl/cert.pem" ] || [ ! -f "ssl/key.pem" ]; then
    print_warning "SSL certificates not found. Generating self-signed certificates..."
    
    # Check if Python is available
    if command -v python3 &> /dev/null; then
        print_status "Using Python to generate SSL certificates..."
        python3 create-test-certs.py
    elif command -v python &> /dev/null; then
        print_status "Using Python to generate SSL certificates..."
        python create-test-certs.py
    else
        print_error "Python is not installed. Please install Python to generate SSL certificates."
        exit 1
    fi
    
    if [ ! -f "ssl/cert.pem" ] || [ ! -f "ssl/key.pem" ]; then
        print_error "Failed to generate SSL certificates."
        exit 1
    fi
    
    print_success "SSL certificates generated successfully"
else
    print_success "SSL certificates found"
fi

# Stop any existing containers
print_status "Stopping any existing containers..."
docker-compose -f docker-compose.https.yml down 2>/dev/null || true

# Remove any existing containers to ensure clean start
print_status "Removing any existing containers..."
docker-compose -f docker-compose.https.yml rm -f 2>/dev/null || true

# Build images if needed
print_status "Building Docker images..."
docker-compose -f docker-compose.https.yml build --no-cache

# Start the services
print_status "Starting NoaMetrics services..."
docker-compose -f docker-compose.https.yml up -d

# Wait for services to be ready
print_status "Waiting for services to start..."
sleep 10

# Check if services are running
print_status "Checking service status..."
if docker-compose -f docker-compose.https.yml ps | grep -q "Up"; then
    print_success "All services are running!"
else
    print_error "Some services failed to start. Check logs with: docker-compose -f docker-compose.https.yml logs"
    exit 1
fi

# Get local IP address
LOCAL_IP=$(hostname -I | awk '{print $1}')
EXTERNAL_IP=$(curl -s ifconfig.me 2>/dev/null || echo "Unable to get external IP")

# Display access information
echo ""
echo "🎉 NoaMetrics is now running with HTTPS!"
echo ""
echo "📱 Access URLs:"
echo "   Local:     https://localhost"
echo "   Network:   https://$LOCAL_IP"
if [ "$EXTERNAL_IP" != "Unable to get external IP" ]; then
    echo "   External:  https://$EXTERNAL_IP (if port forwarding is configured)"
fi
echo ""
echo "🔧 Management Commands:"
echo "   View logs:    docker-compose -f docker-compose.https.yml logs -f"
echo "   Stop:         ./stop-https.sh"
echo "   Status:       docker-compose -f docker-compose.https.yml ps"
echo ""
echo "⚠️  Note: This uses self-signed certificates. Your browser may show a security warning."
echo "   Click 'Advanced' and 'Proceed to localhost' to access the application."
echo ""

print_success "NoaMetrics HTTPS startup completed!" 