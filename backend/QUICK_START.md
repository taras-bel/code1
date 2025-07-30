# 🚀 Quick Start Guide

Быстрый старт для NoaMetrics Backend API.

## ⚡ Быстрая настройка (5 минут)

### 1. Подготовка окружения
```bash
# Клонирование и переход в папку
cd backend

# Создание виртуального окружения
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Настройка переменных окружения
Создайте файл `backend/.env`:

```env
# Supabase (получите на https://supabase.com)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Mistral AI (получите на https://console.mistral.ai)
MISTRAL_API_KEY=sk-your_api_key_here

# JWT (сгенерируйте: python -c "import secrets; print(secrets.token_urlsafe(32))")
SECRET_KEY=your_secret_key_here
```

### 3. Настройка Supabase (одноразово)
1. Создайте проект на [supabase.com](https://supabase.com)
2. Выполните SQL из `SETUP_GUIDE.md` в SQL Editor
3. Создайте bucket `cvs` в Storage

### 4. Запуск
```bash
# Запуск сервера
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Проверка
Откройте http://localhost:8000/docs

## 🔧 Минимальная настройка Supabase

Выполните в SQL Editor:

```sql
-- Создание таблиц
CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES profiles(id),
    job_description TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    results JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE uploaded_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id UUID REFERENCES analyses(id),
    user_id UUID REFERENCES profiles(id),
    filename TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_type TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Создание bucket
-- В Storage создайте bucket с именем 'cvs'
```

## 🧪 Тестирование

### Генерация тестовых файлов
```bash
python generate_test_files.py
```

### Проверка API
```bash
# Health check
curl http://localhost:8000/health

# Swagger UI
open http://localhost:8000/docs
```

## 🚨 Частые проблемы

### Ошибка Mistral API
```
❌ MISTRAL_API_KEY не настроен!
```
**Решение:** Проверьте API ключ в `.env` файле

### Ошибка Supabase
```
RuntimeError: SUPABASE_URL must be set
```
**Решение:** Проверьте URL и ключ в `.env` файле

### Ошибка CORS
```
Access to fetch has been blocked
```
**Решение:** Добавьте домен фронтенда в `CORS_ORIGINS` в `config.py`

## 📚 Следующие шаги

1. **Полная настройка**: См. `SETUP_GUIDE.md`
2. **API документация**: http://localhost:8000/docs
3. **Тестирование**: `python generate_test_files.py`
4. **Production**: См. `README.md`

## 🆘 Нужна помощь?

- 📖 [Полное руководство](SETUP_GUIDE.md)
- 📚 [Документация API](README.md)
- 🐛 [Создать issue](../../issues) 