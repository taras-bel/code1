# 🚀 Production Deployment Guide

Руководство по развертыванию NoaMetrics Backend API в production.

## 📋 Содержание

1. [Подготовка к развертыванию](#подготовка-к-развертыванию)
2. [Docker развертывание](#docker-развертывание)
3. [Cloud развертывание](#cloud-развертывание)
4. [Настройка домена и SSL](#настройка-домена-и-ssl)
5. [Мониторинг и логирование](#мониторинг-и-логирование)
6. [Backup и восстановление](#backup-и-восстановление)
7. [Безопасность](#безопасность)

## 🔧 Подготовка к развертыванию

### 1. Production переменные окружения

Создайте файл `.env.production`:

```env
# Supabase Configuration
SUPABASE_URL=https://your-production-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_production_service_role_key

# Mistral AI Configuration
MISTRAL_API_KEY=sk-your_production_mistral_key

# JWT Configuration
SECRET_KEY=your_very_secure_production_secret_key_64_chars_min

# Database Configuration
DATABASE_URL=postgresql://user:password@host:port/database

# Redis Configuration
REDIS_URL=redis://your-redis-host:6379

# Application Configuration
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# CORS Configuration
CORS_ORIGINS=https://your-frontend-domain.com,https://www.your-domain.com

# Security
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

### 2. Генерация безопасных ключей

```bash
# Генерация SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(64))"

# Генерация дополнительных ключей
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Настройка Supabase для Production

1. **Создайте отдельный проект для production**
2. **Настройте RLS политики строже**:

```sql
-- Более строгие политики для production
CREATE POLICY "Strict user access" ON profiles
    FOR ALL USING (
        auth.uid()::text = id::text AND
        auth.email() = email
    );

-- Ограничение по IP (опционально)
CREATE POLICY "IP restricted access" ON analyses
    FOR ALL USING (
        auth.uid()::text = user_id::text AND
        inet_client_addr() <<= 'your-allowed-ip-range'::inet
    );
```

3. **Настройте мониторинг и алерты**
4. **Включите backup**

## 🐳 Docker развертывание

### 1. Dockerfile

```dockerfile
FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Создание пользователя
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Порт
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Запуск
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Docker Compose

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
    env_file:
      - .env.production
    depends_on:
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  celery:
    build: .
    command: celery -A tasks.celery_app worker --loglevel=info
    environment:
      - ENVIRONMENT=production
    env_file:
      - .env.production
    depends_on:
      - redis
    restart: unless-stopped

  celery-beat:
    build: .
    command: celery -A tasks.celery_app beat --loglevel=info
    environment:
      - ENVIRONMENT=production
    env_file:
      - .env.production
    depends_on:
      - redis
    restart: unless-stopped

volumes:
  redis_data:
```

### 3. Запуск с Docker

```bash
# Сборка и запуск
docker-compose -f docker-compose.prod.yml up -d

# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f app

# Остановка
docker-compose -f docker-compose.prod.yml down
```

## ☁️ Cloud развертывание

### AWS (EC2 + RDS)

1. **Создание EC2 инстанса**:
```bash
# Подключение к инстансу
ssh -i your-key.pem ubuntu@your-ec2-ip

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Клонирование репозитория
git clone your-repo
cd your-repo/backend

# Запуск с Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

2. **Настройка RDS**:
```bash
# Создание RDS инстанса PostgreSQL
# Обновление DATABASE_URL в .env.production
```

3. **Настройка Load Balancer**:
```bash
# Создание Application Load Balancer
# Настройка target groups
# Настройка health checks
```

### Google Cloud Platform

1. **Создание Compute Engine**:
```bash
# Создание VM инстанса
gcloud compute instances create noa-backend \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud

# Подключение
gcloud compute ssh noa-backend --zone=us-central1-a
```

2. **Развертывание с Cloud Run**:
```bash
# Сборка и публикация образа
docker build -t gcr.io/your-project/noa-backend .
docker push gcr.io/your-project/noa-backend

# Развертывание
gcloud run deploy noa-backend \
    --image gcr.io/your-project/noa-backend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

### Heroku

1. **Создание Heroku приложения**:
```bash
# Установка Heroku CLI
# Создание приложения
heroku create your-noa-backend

# Настройка переменных окружения
heroku config:set SUPABASE_URL=your_url
heroku config:set MISTRAL_API_KEY=your_key
heroku config:set SECRET_KEY=your_secret

# Развертывание
git push heroku main
```

2. **Добавление Redis**:
```bash
heroku addons:create heroku-redis:hobby-dev
```

## 🌐 Настройка домена и SSL

### 1. Настройка Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # SSL настройки
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://localhost:8000/health;
        access_log off;
    }
}
```

### 2. SSL сертификат с Let's Encrypt

```bash
# Установка Certbot
sudo apt-get install certbot python3-certbot-nginx

# Получение сертификата
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Автоматическое обновление
sudo crontab -e
# Добавить: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Мониторинг и логирование

### 1. Настройка логирования

```python
# В main.py
import logging
from logging.handlers import RotatingFileHandler

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)s %(levelname)s %(message)s',
    handlers=[
        RotatingFileHandler('logs/app.log', maxBytes=10485760, backupCount=5),
        logging.StreamHandler()
    ]
)
```

### 2. Prometheus метрики

```python
from prometheus_client import Counter, Histogram, generate_latest
from fastapi import Request

# Метрики
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')

@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_LATENCY.observe(duration)
    
    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

### 3. Health checks

```python
@app.get("/health")
async def health_check():
    try:
        # Проверка базы данных
        supabase.table("profiles").select("id").limit(1).execute()
        
        # Проверка Redis
        redis_client.ping()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
```

## 💾 Backup и восстановление

### 1. Supabase Backup

```bash
# Автоматический backup (настроить в Supabase Dashboard)
# Ручной backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# Восстановление
psql $DATABASE_URL < backup_file.sql
```

### 2. Storage Backup

```bash
# Backup файлов из Supabase Storage
# Используйте Supabase CLI или API для экспорта
```

### 3. Автоматизация Backup

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Database backup
pg_dump $DATABASE_URL > $BACKUP_DIR/db_backup_$DATE.sql

# Compress
gzip $BACKUP_DIR/db_backup_$DATE.sql

# Clean old backups (keep last 7 days)
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete
```

## 🔒 Безопасность

### 1. Firewall настройки

```bash
# UFW настройки
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw deny 8000/tcp  # Блокируем прямой доступ к приложению
sudo ufw enable
```

### 2. Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/v1/analysis/")
@limiter.limit("10/minute")
async def create_analysis(request: Request):
    # ...
```

### 3. Security Headers

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# Только доверенные хосты
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["your-domain.com"])

# Принудительный HTTPS
app.add_middleware(HTTPSRedirectMiddleware)
```

### 4. API Key Rotation

```python
# Регулярная ротация ключей
# Настройте автоматическую смену SECRET_KEY
# Используйте переменные окружения для управления ключами
```

## 📈 Масштабирование

### 1. Horizontal Scaling

```yaml
# docker-compose.scale.yml
services:
  app:
    deploy:
      replicas: 3
    environment:
      - WORKER_PROCESSES=4
```

### 2. Load Balancer

```nginx
upstream backend {
    least_conn;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

### 3. Database Connection Pooling

```python
# Настройка пула соединений
from databases import Database

database = Database(
    DATABASE_URL,
    min_size=5,
    max_size=20,
    pool_recycle=3600
)
```

## 🚨 Алерты и уведомления

### 1. Мониторинг ошибок

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1,
)
```

### 2. Email уведомления

```python
import smtplib
from email.mime.text import MIMEText

def send_alert(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = "alerts@your-domain.com"
    msg['To'] = "admin@your-domain.com"
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login("your-email", "your-password")
        server.send_message(msg)
```

## 📞 Поддержка Production

### 1. Логи и отладка

```bash
# Просмотр логов
docker-compose logs -f app

# Просмотр логов Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Мониторинг ресурсов
htop
df -h
free -h
```

### 2. Перезапуск сервисов

```bash
# Перезапуск приложения
docker-compose restart app

# Перезапуск Nginx
sudo systemctl restart nginx

# Перезапуск системы
sudo reboot
```

### 3. Обновление

```bash
# Обновление кода
git pull origin main

# Пересборка и перезапуск
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Проверка работоспособности
curl -f http://localhost:8000/health
``` 