# 🚀 NoaMetrics - AI-Powered Talent Analysis Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-green.svg)](https://vuejs.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)

## 🌟 Overview

NoaMetrics is an advanced AI-powered platform for CV analysis and candidate evaluation. Built with modern technologies, it provides instant fraud detection, skill assessment, and comprehensive candidate scoring.

## ✨ Features

### 🎯 **Core Features**
- **AI-Powered CV Analysis** - Instant fraud detection and skill assessment
- **Real-time Scoring** - Comprehensive candidate evaluation with detailed metrics
- **Multi-format Support** - PDF, DOCX, and text file processing
- **Interactive Dashboard** - Beautiful, responsive interface with real-time updates
- **Candidate Comparison** - Side-by-side analysis and ranking
- **Export Capabilities** - CSV reports and detailed analytics

### 🔧 **Technical Features**
- **HTTPS Support** - Secure connections with SSL/TLS
- **Docker Ready** - Easy deployment with containerization
- **API-First Design** - RESTful API for integrations
- **Background Processing** - Celery-based task queue
- **Real-time Updates** - WebSocket support for live updates
- **Responsive Design** - Works on desktop, tablet, and mobile

### 📊 **Analysis Capabilities**
- **Skill Assessment** - Technical and soft skills evaluation
- **Experience Validation** - Work history verification
- **Achievement Scoring** - Quantified accomplishments analysis
- **Growth Tracking** - Career progression evaluation
- **Cultural Fit** - Company alignment assessment

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   AI Services   │
│   (Vue.js)      │◄──►│   (FastAPI)     │◄──►│   (Mistral AI)  │
│                 │    │                 │    │                 │
│ • Dashboard     │    │ • REST API      │    │ • CV Analysis   │
│ • File Upload   │    │ • Auth System   │    │ • Fraud Detect  │
│ • Real-time UI  │    │ • Task Queue    │    │ • Skill Assess  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Infrastructure │
                    │                 │
                    │ • Docker        │
                    │ • Nginx         │
                    │ • Redis         │
                    │ • PostgreSQL    │
                    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Node.js 18+

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/noa-metrics.git
cd noa-metrics
```

### 2. Environment Setup
```bash
# Copy environment file
cp .env.example .env

# Edit environment variables
nano .env
```

### 3. Start the Application
```bash
# Start with HTTPS (recommended)
./start-https.ps1

# Or start with HTTP
docker-compose up -d
```

### 4. Access the Application
- **Local:** https://localhost
- **Network:** https://[YOUR_IP]
- **Internet:** Configure port forwarding or use ngrok

## 📁 Project Structure

```
noa-metrics/
├── backend/                 # FastAPI backend
│   ├── api/                # API endpoints
│   ├── cv_analysis/        # AI analysis modules
│   ├── database/           # Database models
│   ├── security/           # Authentication
│   └── tasks/              # Background tasks
├── frontend/               # Vue.js frontend
│   ├── components/         # Vue components
│   ├── pages/             # Page components
│   ├── composables/       # Vue composables
│   └── config/            # Configuration
├── docker-compose.yml      # Docker configuration
├── nginx.prod.conf         # Nginx configuration
└── docs/                   # Documentation
```

## 🔧 Configuration

### Environment Variables
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

### HTTPS Setup
```bash
# Generate SSL certificates
python create-test-certs.py

# Start with HTTPS
./start-https.ps1
```

## 🌐 Deployment

### Local Development
```bash
# Development mode
docker-compose up -d

# With hot reload
docker-compose -f docker-compose.dev.yml up
```

### Production Deployment
```bash
# Production build
docker-compose -f docker-compose.prod.yml up -d

# With monitoring
docker-compose -f docker-compose.prod.yml -f docker-compose.monitoring.yml up -d
```

### Cloud Deployment
- **Railway:** `railway up`
- **Render:** Connect GitHub repository
- **Heroku:** `heroku container:push web`
- **DigitalOcean:** Use App Platform

## 📊 API Documentation

### Authentication
```bash
# Register
POST /api/v1/auth/beta-register
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "company_name": "Tech Corp",
  "role": "HR Manager",
  "consent": true
}

# Login
POST /api/v1/auth/login
{
  "email": "john@example.com",
  "password": "password"
}
```

### File Upload
```bash
# Upload CV
POST /api/v1/files/upload
Content-Type: multipart/form-data
Authorization: Bearer <token>

# Upload multiple files
POST /api/v1/files/upload-multiple
```

### Analysis
```bash
# Get analysis results
GET /api/v1/analysis/user/me
Authorization: Bearer <token>

# Get dashboard data
GET /api/v1/analysis/summary-report/me
Authorization: Bearer <token>
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm run test
```

### Integration Tests
```bash
python test_api_endpoints.py
python test_cv_analysis.py
```

## 📈 Performance

### Benchmarks
- **CV Processing:** ~30 seconds per CV
- **API Response:** <200ms average
- **Concurrent Users:** 100+ simultaneous
- **File Upload:** Up to 10MB per file

### Optimization
- **Caching:** Redis-based response caching
- **Background Processing:** Celery task queue
- **CDN:** Static asset optimization
- **Database:** Connection pooling

## 🔒 Security

### Features
- **HTTPS/SSL:** End-to-end encryption
- **JWT Authentication:** Secure token-based auth
- **Rate Limiting:** API protection
- **Input Validation:** XSS and injection protection
- **CORS:** Cross-origin resource sharing

### Best Practices
- Regular security updates
- Environment variable protection
- Input sanitization
- SQL injection prevention
- CSRF protection

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Code Style
- **Python:** Black, flake8
- **JavaScript:** ESLint, Prettier
- **Vue:** Vue Style Guide

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Mistral AI** for advanced language processing
- **Supabase** for backend-as-a-service
- **Vue.js** for the frontend framework
- **FastAPI** for the backend framework

## 📞 Support

- **Documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/yourusername/noa-metrics/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/noa-metrics/discussions)
- **Email:** support@noametrics.com

---

**Made with ❤️ by the NoaMetrics Team**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/noa-metrics?style=social)](https://github.com/yourusername/noa-metrics)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/noa-metrics?style=social)](https://github.com/yourusername/noa-metrics)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/noa-metrics)](https://github.com/yourusername/noa-metrics/issues) 