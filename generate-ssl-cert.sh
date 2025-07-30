#!/bin/bash

# Генерация SSL сертификатов для HTTPS
echo "🔐 Генерация SSL сертификатов для HTTPS..."

# Создаем директорию для сертификатов
mkdir -p ssl

# Генерируем самоподписанный сертификат
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/key.pem \
    -out ssl/cert.pem \
    -subj "/C=RU/ST=Moscow/L=Moscow/O=NoaMetrics/OU=Development/CN=localhost"

echo "✅ SSL сертификаты созданы:"
echo "   - ssl/cert.pem (сертификат)"
echo "   - ssl/key.pem (приватный ключ)"

# Проверяем создание файлов
if [ -f "ssl/cert.pem" ] && [ -f "ssl/key.pem" ]; then
    echo "✅ Сертификаты успешно созданы!"
    echo "🔐 Теперь можно запускать с HTTPS"
else
    echo "❌ Ошибка создания сертификатов"
    exit 1
fi 