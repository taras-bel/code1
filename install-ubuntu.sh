#!/bin/bash

# NoaMetrics Ubuntu Installation Script
# This script installs all dependencies for Ubuntu 24.04 LTS

set -e  # Exit on any error

echo "🔧 Installing NoaMetrics dependencies on Ubuntu 24.04 LTS..."

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

# Update system packages
print_status "Updating system packages..."
apt update
apt upgrade -y

# Install essential packages
print_status "Installing essential packages..."
apt install -y \
    curl \
    wget \
    git \
    unzip \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    pkg-config \
    libssl-dev \
    libffi-dev \
    python3-dev

print_success "Essential packages installed"

# Install Docker
print_status "Installing Docker..."
if ! command -v docker &> /dev/null; then
    # Remove old versions
    apt remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true
    
    # Add Docker's official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Add Docker repository
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker
    apt update
    apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # Start and enable Docker service
    systemctl start docker
    systemctl enable docker
    
    print_success "Docker installed successfully"
else
    print_success "Docker is already installed"
fi

# Install Docker Compose (standalone)
print_status "Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    # Download Docker Compose
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    
    # Make it executable
    chmod +x /usr/local/bin/docker-compose
    
    # Create symlink
    ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
    
    print_success "Docker Compose installed successfully"
else
    print_success "Docker Compose is already installed"
fi

# Install Node.js and npm
print_status "Installing Node.js and npm..."
if ! command -v node &> /dev/null; then
    # Add NodeSource repository
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    
    # Install Node.js
    apt install -y nodejs
    
    print_success "Node.js and npm installed successfully"
else
    print_success "Node.js is already installed"
fi

# Install Python dependencies
print_status "Installing Python dependencies..."
# Install cryptography through apt (system package)
apt install -y python3-cryptography

# Create virtual environment for additional packages if needed
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install additional packages
print_status "Installing additional Python packages in virtual environment..."
source venv/bin/activate
pip install --upgrade pip
pip install cryptography  # Install in venv as backup

print_success "Python dependencies installed"

# Create project directory structure
print_status "Setting up project structure..."
mkdir -p ssl
mkdir -p logs

# Set proper permissions
chmod +x start-https.sh
chmod +x stop-https.sh
chmod +x install-ubuntu.sh

print_success "Project structure created"

# Install UFW firewall (optional but recommended)
print_status "Setting up firewall..."
if ! command -v ufw &> /dev/null; then
    apt install -y ufw
    ufw --force enable
    ufw allow ssh
    ufw allow 80/tcp
    ufw allow 443/tcp
    print_success "Firewall configured"
else
    print_success "Firewall is already installed"
fi

# Install monitoring tools (optional)
print_status "Installing monitoring tools..."
apt install -y htop iotop nethogs

print_success "Monitoring tools installed"

# Display installation summary
echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📋 Installed components:"
echo "   ✅ System packages updated"
echo "   ✅ Docker and Docker Compose"
echo "   ✅ Node.js and npm"
echo "   ✅ Python and dependencies"
echo "   ✅ Firewall (UFW)"
echo "   ✅ Monitoring tools"
echo ""
echo "🔧 Next steps:"
echo "   1. Copy your .env file: cp .env.example .env"
echo "   2. Edit .env with your configuration"
echo "   3. Start the application: ./start-https.sh"
echo ""
echo "📚 Useful commands:"
echo "   Start:     ./start-https.sh"
echo "   Stop:      ./stop-https.sh"
echo "   Status:    docker-compose -f docker-compose.https.yml ps"
echo "   Logs:      docker-compose -f docker-compose.https.yml logs -f"
echo "   Clean:     docker system prune -a"
echo ""
echo "🌐 Access URLs (after starting):"
echo "   Local:     https://localhost"
echo "   Network:   https://$(hostname -I | awk '{print $1}')"
echo ""

print_success "NoaMetrics installation completed!" 