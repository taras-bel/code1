#!/bin/bash

# Setup External Access for NoaMetrics
# This script helps configure the application for external access

set -e

print_status() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

print_success() {
    echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}

print_warning() {
    echo -e "\033[1;33m[WARNING]\033[0m $1"
}

print_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

echo "🔧 Setting up external access for NoaMetrics..."

# Get external IP
print_status "Getting external IP address..."
if command -v curl &> /dev/null; then
    EXTERNAL_IP=$(curl -s ifconfig.me)
elif command -v wget &> /dev/null; then
    EXTERNAL_IP=$(wget -qO- ifconfig.me)
else
    print_error "Neither curl nor wget found. Please enter external IP manually:"
    read -r EXTERNAL_IP
fi

if [ -z "$EXTERNAL_IP" ]; then
    print_error "Failed to get external IP. Please enter it manually:"
    read -r EXTERNAL_IP
else
    print_success "External IP: $EXTERNAL_IP"
fi

# Get local IP
print_status "Getting local IP address..."
LOCAL_IP=$(hostname -I | awk '{print $1}')

if [ -z "$LOCAL_IP" ]; then
    print_error "Failed to get local IP. Please enter it manually:"
    read -r LOCAL_IP
else
    print_success "Local IP: $LOCAL_IP"
fi

# Create or update .env file
print_status "Updating environment configuration..."

ENV_CONTENT="# External Access Configuration
EXTERNAL_IPS=$EXTERNAL_IP,$LOCAL_IP

# Add your external IP to CORS origins
# The application will automatically allow access from these IPs"

# Check if .env exists
if [ -f ".env" ]; then
    print_status "Updating existing .env file..."
    
    # Check if EXTERNAL_IPS already exists
    if grep -q "EXTERNAL_IPS=" .env; then
        # Update existing EXTERNAL_IPS
        sed -i "s/EXTERNAL_IPS=.*/EXTERNAL_IPS=$EXTERNAL_IP,$LOCAL_IP/" .env
    else
        # Add EXTERNAL_IPS to existing file
        echo "" >> .env
        echo "# External Access Configuration" >> .env
        echo "EXTERNAL_IPS=$EXTERNAL_IP,$LOCAL_IP" >> .env
    fi
else
    print_status "Creating new .env file..."
    echo "$ENV_CONTENT" > .env
fi

print_success "Environment configuration updated!"

# Display access information
echo ""
echo "🌐 Access Information:"
echo "   Local Access:     https://localhost"
echo "   Network Access:   https://$LOCAL_IP"
echo "   External Access:  https://$EXTERNAL_IP"

echo ""
echo "🔧 Next Steps:"
echo "   1. Restart the application: ./stop-https.sh && ./start-https.sh"
echo "   2. Configure firewall (if needed):"
echo "      - sudo ufw allow 80/tcp"
echo "      - sudo ufw allow 443/tcp"
echo "   3. Test external access: https://$EXTERNAL_IP"

echo ""
print_success "External access setup complete!" 