# 🐧 Ubuntu 24.04 LTS Deployment Guide

## 📋 Prerequisites

- Ubuntu 24.04 LTS server
- User with sudo privileges
- Internet connection
- At least 2GB RAM and 10GB disk space

## 🚀 Quick Start

### 1. Clone the Repository

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/noa-metrics.git
cd noa-metrics

# Make scripts executable
chmod +x *.sh
```

### 2. Install Dependencies

```bash
# Run the installation script
./install-ubuntu.sh
```

**Note:** You'll need to log out and log back in after installation for Docker group changes to take effect.

### 3. Configure Environment

```bash
# Copy environment file
cp .env.example .env

# Edit environment variables
nano .env
```

### 4. Start the Application

```bash
# Start with HTTPS
./start-https.sh
```

## 🔧 Detailed Installation

### Manual Installation Steps

If you prefer to install manually:

#### 1. Update System

```bash
sudo apt update
sudo apt upgrade -y
```

#### 2. Install Essential Packages

```bash
sudo apt install -y \
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
```

#### 3. Install Docker

```bash
# Remove old versions
sudo apt remove -y docker docker-engine docker.io containerd runc

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
```

#### 4. Install Docker Compose

```bash
# Download Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make it executable
sudo chmod +x /usr/local/bin/docker-compose

# Create symlink
sudo ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
```

#### 5. Install Node.js

```bash
# Add NodeSource repository
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -

# Install Node.js
sudo apt install -y nodejs
```

#### 6. Install Python Dependencies

```bash
pip3 install --user --upgrade pip
pip3 install --user cryptography
```

#### 7. Set Up Firewall

```bash
sudo apt install -y ufw
sudo ufw --force enable
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

## 🌐 Configuration

### Environment Variables

Edit the `.env` file with your configuration:

```bash
# Database
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_key

# AI Services
MISTRAL_API_KEY=your_mistral_key

# Security
SECRET_KEY=your_secret_key

# Redis
REDIS_URL=redis://redis:6379
```

### SSL Certificates

The application will automatically generate self-signed certificates on first run. For production, consider using Let's Encrypt:

```bash
# Install Certbot
sudo apt install -y certbot

# Get SSL certificate (replace with your domain)
sudo certbot certonly --standalone -d yourdomain.com

# Copy certificates to ssl directory
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/key.pem
sudo chown $USER:$USER ssl/cert.pem ssl/key.pem
```

## 🚀 Management Commands

### Start Application

```bash
./start-https.sh
```

### Stop Application

```bash
./stop-https.sh
```

### Check Status

```bash
docker-compose -f docker-compose.https.yml ps
```

### View Logs

```bash
# All services
docker-compose -f docker-compose.https.yml logs -f

# Specific service
docker-compose -f docker-compose.https.yml logs -f backend
docker-compose -f docker-compose.https.yml logs -f frontend
docker-compose -f docker-compose.https.yml logs -f nginx
```

### Update Application

```bash
./update-ubuntu.sh
```

### Restart Application

```bash
./stop-https.sh && ./start-https.sh
```

## 🔒 Security Configuration

### Firewall Setup

```bash
# Check firewall status
sudo ufw status

# Allow additional ports if needed
sudo ufw allow 3000/tcp  # Frontend development
sudo ufw allow 8000/tcp  # Backend development

# Enable logging
sudo ufw logging on
```

### SSL/TLS Configuration

For production, update the Nginx configuration:

```bash
# Edit Nginx configuration
sudo nano nginx.prod.conf

# Update SSL certificate paths
ssl_certificate /path/to/your/cert.pem;
ssl_certificate_key /path/to/your/key.pem;
```

### System Security

```bash
# Install fail2ban
sudo apt install -y fail2ban

# Configure fail2ban
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## 📊 Monitoring

### System Monitoring

```bash
# Install monitoring tools
sudo apt install -y htop iotop nethogs

# Monitor system resources
htop
iotop
nethogs
```

### Application Monitoring

```bash
# Check container resource usage
docker stats

# Monitor disk usage
df -h

# Monitor memory usage
free -h
```

### Log Monitoring

```bash
# Set up log rotation
sudo nano /etc/logrotate.d/noa-metrics

# Add configuration
/path/to/noa-metrics/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 $USER $USER
}
```

## 🔄 Backup and Recovery

### Backup Configuration

```bash
# Create backup script
nano backup-noa-metrics.sh

# Add backup commands
#!/bin/bash
BACKUP_DIR="/backup/noa-metrics/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Backup configuration
cp .env $BACKUP_DIR/
cp -r ssl $BACKUP_DIR/

# Backup database (if using local database)
docker-compose -f docker-compose.https.yml exec -T backend pg_dump > $BACKUP_DIR/database.sql

# Compress backup
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
rm -rf $BACKUP_DIR

echo "Backup created: $BACKUP_DIR.tar.gz"
```

### Recovery

```bash
# Restore from backup
tar -xzf backup-file.tar.gz
cp backup/.env .
cp -r backup/ssl .
```

## 🐛 Troubleshooting

### Common Issues

#### Docker Permission Denied

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and log back in, or run:
newgrp docker
```

#### Port Already in Use

```bash
# Check what's using the port
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443

# Kill the process
sudo kill -9 PID
```

#### SSL Certificate Issues

```bash
# Regenerate certificates
python3 create-test-certs.py

# Check certificate validity
openssl x509 -in ssl/cert.pem -text -noout
```

#### Container Won't Start

```bash
# Check container logs
docker-compose -f docker-compose.https.yml logs

# Rebuild containers
docker-compose -f docker-compose.https.yml build --no-cache

# Remove and recreate containers
docker-compose -f docker-compose.https.yml down -v
docker-compose -f docker-compose.https.yml up -d
```

### Performance Issues

#### High Memory Usage

```bash
# Check memory usage
free -h

# Optimize Docker
docker system prune -a

# Adjust container limits in docker-compose.https.yml
```

#### High CPU Usage

```bash
# Check CPU usage
top

# Monitor specific containers
docker stats

# Optimize application settings
```

## 📈 Production Optimization

### Performance Tuning

```bash
# Optimize system settings
sudo nano /etc/sysctl.conf

# Add optimizations
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535
net.core.netdev_max_backlog = 65535
```

### Load Balancing

For high-traffic deployments, consider using a load balancer:

```bash
# Install HAProxy
sudo apt install -y haproxy

# Configure HAProxy
sudo nano /etc/haproxy/haproxy.cfg
```

### Auto-scaling

Set up auto-scaling with systemd:

```bash
# Create systemd service
sudo nano /etc/systemd/system/noa-metrics.service

# Enable auto-start
sudo systemctl enable noa-metrics
sudo systemctl start noa-metrics
```

## 🎯 Next Steps

### 1. Domain Configuration

- Point your domain to the server IP
- Configure DNS records
- Set up SSL certificates with Let's Encrypt

### 2. Monitoring Setup

- Install Prometheus and Grafana
- Set up alerting
- Configure log aggregation

### 3. Backup Strategy

- Set up automated backups
- Test recovery procedures
- Configure off-site storage

### 4. Security Hardening

- Regular security updates
- Intrusion detection
- Vulnerability scanning

---

**Your NoaMetrics application is now running on Ubuntu 24.04 LTS! 🚀**

For support, check the [GitHub Issues](https://github.com/YOUR_USERNAME/noa-metrics/issues) or create a new one. 