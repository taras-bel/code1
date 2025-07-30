# NoaMetrics Backend Setup Guide

Подробное руководство по настройке NoaMetrics Backend API.

## 📋 Содержание

1. [Предварительные требования](#предварительные-требования)
2. [Установка зависимостей](#установка-зависимостей)
3. [Настройка Supabase](#настройка-supabase)
4. [Настройка Mistral AI](#настройка-mistral-ai)
5. [Конфигурация приложения](#конфигурация-приложения)
6. [Запуск системы](#запуск-системы)
7. [Тестирование](#тестирование)
8. [Устранение неполадок](#устранение-неполадок)

## 🔧 Предварительные требования

### Системные требования
- **Python**: 3.8 или выше
- **ОС**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **RAM**: Минимум 2GB (рекомендуется 4GB+)
- **Дисковое пространство**: 1GB свободного места

### Необходимые аккаунты
- [Supabase](https://supabase.com) - для базы данных и хранилища
- [Mistral AI](https://console.mistral.ai) - для AI анализа

## 📦 Установка зависимостей

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd noa-landing-backend-v0-main/backend
```

### 2. Создание виртуального окружения
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка Python зависимостей
```bash
pip install -r requirements.txt
```

### 4. Установка дополнительных зависимостей (если нужно)
```bash
# Для работы с PDF
pip install PyPDF2

# Для работы с DOCX
pip install python-docx

# Для шрифтов (если генерируете PDF)
# Скачайте DejaVuSans.ttf и поместите в backend/fonts/
```

## 🗄️ Настройка Supabase

### 1. Создание проекта
1. Перейдите на [supabase.com](https://supabase.com)
2. Создайте новый проект
3. Запишите URL проекта и Service Role Key

### 2. Создание таблиц
Выполните следующие SQL команды в Supabase SQL Editor:

```sql
-- Включение расширений
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Таблица профилей пользователей
CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    phone TEXT,
    company_name TEXT,
    role TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Таблица анализов
CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    job_description TEXT NOT NULL,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
    results JSONB,
    error_message TEXT,
    processing_time FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Таблица загруженных файлов
CREATE TABLE uploaded_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id UUID REFERENCES analyses(id) ON DELETE CASCADE,
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_type TEXT NOT NULL,
    file_size INTEGER,
    mime_type TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Таблица лимитов использования
CREATE TABLE rate_limits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    action TEXT NOT NULL,
    count INTEGER DEFAULT 0,
    reset_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, action)
);

-- Индексы для производительности
CREATE INDEX idx_analyses_user_id ON analyses(user_id);
CREATE INDEX idx_analyses_status ON analyses(status);
CREATE INDEX idx_uploaded_files_analysis_id ON uploaded_files(analysis_id);
CREATE INDEX idx_rate_limits_user_action ON rate_limits(user_id, action);
```

### 3. Настройка Row Level Security (RLS)
```sql
-- Включение RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE uploaded_files ENABLE ROW LEVEL SECURITY;
ALTER TABLE rate_limits ENABLE ROW LEVEL SECURITY;

-- Политики для profiles
CREATE POLICY "Users can view own profile" ON profiles
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth.uid()::text = id::text);

CREATE POLICY "Users can insert own profile" ON profiles
    FOR INSERT WITH CHECK (auth.uid()::text = id::text);

-- Политики для analyses
CREATE POLICY "Users can view own analyses" ON analyses
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert own analyses" ON analyses
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update own analyses" ON analyses
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete own analyses" ON analyses
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- Политики для uploaded_files
CREATE POLICY "Users can view own files" ON uploaded_files
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert own files" ON uploaded_files
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete own files" ON uploaded_files
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- Политики для rate_limits
CREATE POLICY "Users can view own rate limits" ON rate_limits
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert own rate limits" ON rate_limits
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update own rate limits" ON rate_limits
    FOR UPDATE USING (auth.uid()::text = user_id::text);
```

### 4. Создание Storage Bucket
1. Перейдите в раздел Storage в Supabase Dashboard
2. Создайте новый bucket с именем `cvs`
3. Настройте политики доступа:

```sql
-- Политика для загрузки файлов
CREATE POLICY "Users can upload files" ON storage.objects
    FOR INSERT WITH CHECK (
        bucket_id = 'cvs' AND 
        auth.uid()::text = (storage.foldername(name))[1]
    );

-- Политика для просмотра файлов
CREATE POLICY "Users can view own files" ON storage.objects
    FOR SELECT USING (
        bucket_id = 'cvs' AND 
        auth.uid()::text = (storage.foldername(name))[1]
    );

-- Политика для удаления файлов
CREATE POLICY "Users can delete own files" ON storage.objects
    FOR DELETE USING (
        bucket_id = 'cvs' AND 
        auth.uid()::text = (storage.foldername(name))[1]
    );
```

## 🤖 Настройка Mistral AI

### 1. Получение API ключа
1. Перейдите на [console.mistral.ai](https://console.mistral.ai)
2. Создайте аккаунт или войдите в существующий
3. Перейдите в раздел API Keys
4. Создайте новый API ключ
5. Скопируйте ключ (он начинается с `sk-`)

### 2. Проверка модели
Система использует модель `mistral-large-latest` по умолчанию. Убедитесь, что у вас есть доступ к этой модели.

## ⚙️ Конфигурация приложения

### 1. Создание файла .env
Создайте файл `backend/.env` со следующим содержимым:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

# Mistral AI Configuration
MISTRAL_API_KEY=sk-your_mistral_api_key_here

# JWT Configuration
SECRET_KEY=your_very_secure_secret_key_here_make_it_long_and_random

# Optional: Redis for Celery (если используете фоновые задачи)
REDIS_URL=redis://localhost:6379

# Optional: Logging
LOG_LEVEL=INFO
```

### 2. Генерация секретного ключа
Для генерации безопасного SECRET_KEY используйте:

```python
import secrets
print(secrets.token_urlsafe(32))
```

### 3. Создание папки для шрифтов (опционально)
```bash
mkdir backend/fonts
# Скачайте DejaVuSans.ttf и поместите в эту папку
```

## 🚀 Запуск системы

### 1. Проверка конфигурации
```bash
cd backend
python -c "from config import *; print('Configuration loaded successfully')"
```

### 2. Запуск в режиме разработки
```bash
# Запуск FastAPI сервера
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# В отдельном терминале (опционально) - Celery worker
celery -A tasks.celery_app worker --loglevel=info

# В отдельном терминале (опционально) - Celery beat
celery -A tasks.celery_app beat --loglevel=info
```

### 3. Проверка работоспособности
Откройте браузер и перейдите на:
- http://localhost:8000/health - проверка состояния
- http://localhost:8000/docs - Swagger документация

## 🧪 Тестирование

### 1. Генерация тестовых файлов
```bash
python generate_test_files.py
```

### 2. Запуск тестов
```bash
pytest
```

### 3. Тестирование API
```bash
# Тест загрузки файла
curl -X POST "http://localhost:8000/api/v1/files/upload" \
  -H "Authorization: Bearer your_token" \
  -F "file=@test_files/cv_candidate_1.pdf" \
  -F "analysis_id=your_analysis_id"
```

## 🚨 Устранение неполадок

### Ошибки Mistral API

**Ошибка 401 Unauthorized**
```
❌ Неверный MISTRAL_API_KEY! Проверьте правильность ключа в backend/.env
```
**Решение:**
- Проверьте правильность API ключа
- Убедитесь, что ключ не содержит лишних символов
- Проверьте баланс аккаунта Mistral

**Ошибка 429 Too Many Requests**
```
❌ Превышен лимит запросов к Mistral API
```
**Решение:**
- Подождите несколько минут
- Проверьте лимиты вашего аккаунта
- Увеличьте паузы между запросами

### Ошибки Supabase

**Ошибка подключения к Supabase**
```
RuntimeError: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set
```
**Решение:**
- Проверьте переменные окружения
- Убедитесь, что проект Supabase активен
- Проверьте правильность URL и ключа

**Ошибка 403 Forbidden при загрузке файлов**
```
Failed to upload file to storage
```
**Решение:**
- Проверьте политики RLS в Supabase
- Убедитесь, что bucket `cvs` существует
- Проверьте права доступа к Storage

### Ошибки CORS

**Ошибка CORS в браузере**
```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked
```
**Решение:**
- Обновите CORS_ORIGINS в config.py
- Добавьте домен фронтенда в список разрешенных

### Ошибки файлов

**Ошибка при загрузке файла**
```
File type not allowed
```
**Решение:**
- Убедитесь, что файл имеет расширение .pdf, .docx или .doc
- Проверьте размер файла (максимум 10MB)

**Ошибка при извлечении текста**
```
Error extracting PDF text
```
**Решение:**
- Убедитесь, что PDF не защищен паролем
- Проверьте, что PDF содержит текст (не изображения)
- Установите PyPDF2: `pip install PyPDF2`

## 📞 Поддержка

Если у вас возникли проблемы:

1. **Проверьте логи** - они содержат подробную информацию об ошибках
2. **Создайте issue** в репозитории проекта
3. **Опишите проблему** с указанием:
   - Версии Python
   - Операционной системы
   - Полного текста ошибки
   - Шагов для воспроизведения

## 🔄 Обновления

Для обновления системы:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

Проверьте изменения в конфигурации и обновите .env файл при необходимости. 