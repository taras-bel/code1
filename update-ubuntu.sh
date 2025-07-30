#!/bin/bash

# NoaMetrics Ubuntu Update Script
# This script updates the application and dependencies

set -e  # Exit on any error

echo "🔄 Updating NoaMetrics on Ubuntu..."

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

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "This script must be run as root. Please run with sudo or as root user."
    exit 1
fi

# Check if we're in the project directory
if [ ! -f "docker-compose.https.yml" ]; then
    print_error "docker-compose.https.yml not found. Are you in the correct directory?"
    exit 1
fi

# Stop the application if it's running
print_status "Stopping running application..."
if docker-compose -f docker-compose.https.yml ps | grep -q "Up"; then
    ./stop-https.sh
    sleep 5
else
    print_status "Application is not running"
fi

# Update system packages
print_status "Updating system packages..."
apt update
apt upgrade -y

# Update Docker
print_status "Updating Docker..."
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Update Docker Compose
print_status "Updating Docker Compose..."
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose

# Update Node.js
print_status "Updating Node.js..."
if command -v node &> /dev/null; then
    # Add NodeSource repository for latest version
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt install -y nodejs
else
    print_warning "Node.js not found, installing..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt install -y nodejs
fi

# Update Python packages
print_status "Updating Python packages..."
pip3 install --upgrade pip
pip3 install --upgrade cryptography

# Clean up Docker
print_status "Cleaning up Docker..."
docker system prune -f
docker image prune -f

# Pull latest images
print_status "Pulling latest Docker images..."
docker-compose -f docker-compose.https.yml pull

# Rebuild images
print_status "Rebuilding Docker images..."
docker-compose -f docker-compose.https.yml build --no-cache

# Update SSL certificates if needed
print_status "Checking SSL certificates..."
if [ ! -f "ssl/cert.pem" ] || [ ! -f "ssl/key.pem" ]; then
    print_warning "SSL certificates not found, generating new ones..."
    if command -v python3 &> /dev/null; then
        python3 create-test-certs.py
    elif command -v python &> /dev/null; then
        python create-test-certs.py
    else
        print_error "Python not found, cannot generate SSL certificates"
        exit 1
    fi
fi

# Start the application
print_status "Starting updated application..."
./start-https.sh

# Display update summary
echo ""
echo "🎉 Update completed successfully!"
echo ""
echo "📋 Updated components:"
echo "   ✅ System packages"
echo "   ✅ Docker and Docker Compose"
echo "   ✅ Node.js and npm"
echo "   ✅ Python packages"
echo "   ✅ Docker images"
echo "   ✅ SSL certificates"
echo ""
echo "📊 System status:"
echo "   Docker version: $(docker --version)"
echo "   Docker Compose version: $(docker-compose --version)"
echo "   Node.js version: $(node --version)"
echo "   npm version: $(npm --version)"
echo "   Python version: $(python3 --version)"
echo ""
echo "🌐 Application status:"
docker-compose -f docker-compose.https.yml ps
echo ""
echo "📚 Useful commands:"
echo "   View logs:    docker-compose -f docker-compose.https.yml logs -f"
echo "   Stop:         ./stop-https.sh"
echo "   Restart:      ./stop-https.sh && ./start-https.sh"
echo "   Clean:        docker system prune -a"
echo ""

print_success "NoaMetrics update completed!" 