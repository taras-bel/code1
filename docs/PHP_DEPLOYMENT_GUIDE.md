# 🚀 NoaMetrics PHP Backend - Руководство по развертыванию на IONOS

Полное руководство по развертыванию NoaMetrics с PHP бэкендом на IONOS сервере.

## 📋 Содержание

1. [Преимущества PHP версии](#преимущества-php-версии)
2. [Требования](#требования)
3. [Быстрое развертывание](#быстрое-развертывание)
4. [Ручное развертывание](#ручное-развертывание)
5. [Настройка API ключей](#настройка-api-ключей)
6. [Управление сервисами](#управление-сервисами)
7. [Обновление](#обновление)
8. [Устранение неполадок](#устранение-неполадок)

## 🎯 Преимущества PHP версии

### По сравнению с Python + Docker:

| Аспект | Python + Docker | PHP |
|--------|----------------|-----|
| **Сложность развертывания** | Высокая | Низкая |
| **Стоимость хостинга** | Высокая | Низкая |
| **Производительность** | Хорошая | Хорошая |
| **Масштабируемость** | Отличная | Хорошая |
| **Поддержка IONOS** | Ограниченная | Отличная |
| **Время разработки** | Долгое | Быстрое |

### Ключевые преимущества:

- ✅ **Простота развертывания** - просто загрузил файлы
- ✅ **Дешевле хостинг** - не нужен VPS
- ✅ **Лучше поддержка** - IONOS оптимизирован для PHP
- ✅ **Быстрее разработка** - меньше конфигурации
- ✅ **Встроенная поддержка** - Apache + PHP из коробки

## 🔧 Требования

### Системные требования:
- **ОС**: Ubuntu 20.04 LTS или новее
- **RAM**: Минимум 2GB (рекомендуется 4GB)
- **CPU**: 1 ядро (рекомендуется 2 ядра)
- **Диск**: 20GB свободного места

### Программное обеспечение:
- **PHP**: 8.1 или новее
- **Nginx**: Последняя версия
- **Node.js**: 18.x или новее (для сборки фронтенда)
- **Certbot**: Для SSL сертификатов

## ⚡ Быстрое развертывание

### Вариант 1: Автоматическое развертывание с Windows

```powershell
# Запуск PowerShell скрипта
.\deploy\deploy-ionos-php.ps1 -ServerIP "YOUR_SERVER_IP" -Username "root"
```

### Вариант 2: Автоматическое развертывание с Linux

```bash
# Загрузка проекта на сервер
scp -r . root@YOUR_SERVER_IP:/tmp/noa-metrics-php/

# Подключение к серверу
ssh root@YOUR_SERVER_IP

# Запуск скрипта развертывания
cd /tmp/noa-metrics-php
chmod +x deploy/deploy-ionos-php.sh
./deploy/deploy-ionos-php.sh
```

## 🛠️ Ручное развертывание

### Шаг 1: Подготовка сервера

```bash
# Обновление системы
apt update && apt upgrade -y

# Установка необходимых пакетов
apt install -y nginx php8.1-fpm php8.1-curl php8.1-json php8.1-mbstring php8.1-xml php8.1-zip php8.1-mysql certbot python3-certbot-nginx ufw

# Установка Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs
```

### Шаг 2: Создание структуры директорий

```bash
# Создание директорий
mkdir -p /NoaMetrics/var/www/noa-landing-backend
mkdir -p /NoaMetrics/var/www/noa-landing-backend/backend
mkdir -p /NoaMetrics/var/www/noa-landing-backend/frontend
mkdir -p /var/log/noa-metrics

# Настройка прав доступа
chown -R www-data:www-data /NoaMetrics/var/www/noa-landing-backend
chmod -R 755 /NoaMetrics/var/www/noa-landing-backend
```

### Шаг 3: Развертывание бэкенда

```bash
# Копирование PHP файлов
cp -r backend/* /NoaMetrics/var/www/noa-landing-backend/backend/

# Настройка конфигурации
nano /NoaMetrics/var/www/noa-landing-backend/backend/config/config.php
```

### Шаг 4: Развертывание фронтенда

```bash
# Копирование фронтенда
cp -r frontend/* /NoaMetrics/var/www/noa-landing-backend/frontend/

# Сборка фронтенда
cd /NoaMetrics/var/www/noa-landing-backend/frontend
npm install
npm run build

# Копирование собранных файлов
cp -r .output/public/* /NoaMetrics/var/www/noa-landing-backend/frontend/
```

### Шаг 5: Настройка Nginx

```bash
# Создание конфигурации сайта
cat > /etc/nginx/sites-available/noametrics.com << 'EOF'
server {
    listen 80;
    server_name noametrics.com www.noametrics.com;
    
    # Логи
    access_log /var/log/nginx/noametrics.com.access.log;
    error_log /var/log/nginx/noametrics.com.error.log;
    
    # Фронтенд
    location / {
        root /NoaMetrics/var/www/noa-landing-backend/frontend;
        try_files $uri $uri/ /index.html;
        
        # Кэширование статических файлов
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
    
    # API запросы
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS заголовки
        add_header Access-Control-Allow-Origin * always;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
        add_header Access-Control-Allow-Headers "Content-Type, Authorization, X-Requested-With" always;
    }
    
    # Безопасность
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Сжатие
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
}
EOF

# Активация сайта
ln -sf /etc/nginx/sites-available/noametrics.com /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Проверка конфигурации
nginx -t

# Перезапуск Nginx
systemctl reload nginx
```

### Шаг 6: Настройка PHP сервиса

```bash
# Создание systemd сервиса
cat > /etc/systemd/system/noa-metrics-php.service << 'EOF'
[Unit]
Description=NoaMetrics PHP Backend
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/NoaMetrics/var/www/noa-landing-backend/backend
ExecStart=/usr/bin/php -S 127.0.0.1:8000
Restart=always
RestartSec=10
Environment=PATH=/usr/bin:/usr/local/bin

[Install]
WantedBy=multi-user.target
EOF

# Запуск сервиса
systemctl daemon-reload
systemctl enable noa-metrics-php
systemctl start noa-metrics-php
```

### Шаг 7: Настройка SSL

```bash
# Получение SSL сертификата
certbot --nginx -d noametrics.com -d www.noametrics.com --non-interactive --agree-tos --email admin@noametrics.com

# Настройка firewall
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
```

## 🔑 Настройка API ключей

### Шаг 1: Редактирование конфигурации

```bash
nano /NoaMetrics/var/www/noa-landing-backend/backend/config/config.php
```

### Шаг 2: Замена значений

```php
<?php
// Замените на ваши реальные значения

// Supabase
define('SUPABASE_URL', 'https://your-project.supabase.co');
define('SUPABASE_ANON_KEY', 'your-anon-key');
define('SUPABASE_SERVICE_ROLE_KEY', 'your-service-role-key');

// Mistral AI
define('MISTRAL_API_KEY', 'your-mistral-api-key');
define('MISTRAL_API_URL', 'https://api.mistral.ai/v1');

// Безопасность
define('SECRET_KEY', 'your-secret-key-here-make-it-long-and-random');
define('JWT_SECRET', 'your-jwt-secret-key');
?>
```

### Шаг 3: Перезапуск сервиса

```bash
systemctl restart noa-metrics-php
```

## 🎛️ Управление сервисами

### Проверка статуса

```bash
# Статус всех сервисов
systemctl status nginx
systemctl status php8.1-fpm
systemctl status noa-metrics-php

# Логи сервисов
journalctl -u noa-metrics-php -f
tail -f /var/log/nginx/noametrics.com.error.log
tail -f /var/log/noa-metrics/php_errors.log
```

### Перезапуск сервисов

```bash
# Перезапуск Nginx
systemctl reload nginx

# Перезапуск PHP сервиса
systemctl restart noa-metrics-php

# Перезапуск PHP-FPM
systemctl reload php8.1-fpm
```

### Остановка/Запуск

```bash
# Остановка
systemctl stop noa-metrics-php

# Запуск
systemctl start noa-metrics-php

# Включение автозапуска
systemctl enable noa-metrics-php
```

## 🔄 Обновление

### Автоматическое обновление

```bash
# Использование скрипта обновления
/NoaMetrics/var/www/noa-landing-backend/update.sh
```

### Ручное обновление

```bash
# Остановка сервиса
systemctl stop noa-metrics-php

# Обновление фронтенда
cd /NoaMetrics/var/www/noa-landing-backend/frontend
npm install
npm run build

# Обновление бэкенда (замените файлы)
cp -r /path/to/new/backend/* /NoaMetrics/var/www/noa-landing-backend/backend/

# Обновление прав доступа
chown -R www-data:www-data /NoaMetrics/var/www/noa-landing-backend
chmod -R 755 /NoaMetrics/var/www/noa-landing-backend

# Перезапуск сервисов
systemctl start noa-metrics-php
systemctl reload nginx
```

## 🔧 Устранение неполадок

### Проблема: Сайт не загружается

```bash
# Проверка статуса Nginx
systemctl status nginx

# Проверка конфигурации Nginx
nginx -t

# Проверка логов
tail -f /var/log/nginx/noametrics.com.error.log
```

### Проблема: API не отвечает

```bash
# Проверка статуса PHP сервиса
systemctl status noa-metrics-php

# Проверка логов PHP
journalctl -u noa-metrics-php -f

# Проверка порта
netstat -tlnp | grep :8000
```

### Проблема: Ошибки PHP

```bash
# Проверка логов PHP
tail -f /var/log/noa-metrics/php_errors.log

# Проверка конфигурации PHP
php -l /NoaMetrics/var/www/noa-landing-backend/backend/config/config.php
```

### Проблема: SSL сертификат

```bash
# Проверка SSL сертификата
certbot certificates

# Обновление SSL сертификата
certbot renew

# Проверка автоматического обновления
systemctl status certbot.timer
```

## 📊 Мониторинг

### Проверка здоровья API

```bash
# Проверка API
curl https://noametrics.com/api/v1/health

# Ожидаемый ответ:
{
  "status": "healthy",
  "timestamp": "2024-01-01 12:00:00",
  "version": "1.0.0",
  "services": {
    "api": "ok",
    "database": "ok",
    "mistral_ai": "ok"
  }
}
```

### Мониторинг ресурсов

```bash
# Использование CPU и RAM
htop

# Использование диска
df -h

# Логи в реальном времени
tail -f /var/log/nginx/noametrics.com.access.log
```

## 🎉 Готово!

После успешного развертывания:

- 🌐 **Сайт**: https://noametrics.com
- 🔧 **API**: https://noametrics.com/api/v1/health
- 📝 **Логи**: `/var/log/noa-metrics/`
- 🔄 **Обновления**: `/NoaMetrics/var/www/noa-landing-backend/update.sh`

### Следующие шаги:

1. ✅ Настройте API ключи в конфигурации
2. ✅ Протестируйте все функции
3. ✅ Настройте мониторинг
4. ✅ Настройте резервное копирование
5. ✅ Документируйте изменения

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи сервисов
2. Убедитесь в правильности конфигурации
3. Проверьте статус всех сервисов
4. Обратитесь к документации
5. Создайте Issue в репозитории 