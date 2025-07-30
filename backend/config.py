import os
from dotenv import load_dotenv

# Загружаем .env файл
load_dotenv()

def get_mistral_api_key():
    """Получает API ключ Mistral из переменных окружения"""
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key or api_key == "sk-...":
        raise ValueError(
            "❌ MISTRAL_API_KEY не настроен!\n"
            "1. Получите API ключ на https://console.mistral.ai/\n"
            "2. Создайте файл backend/.env\n"
            "3. Добавьте: MISTRAL_API_KEY=ваш_ключ_здесь"
        )
    return api_key

# Supabase конфигурация
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Mistral AI конфигурация
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-small-latest"

# Storage конфигурация
BUCKET_NAME = "cvs"

# JWT конфигурация
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Лимиты
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ANALYSIS_LIMIT_PER_WEEK = 4
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.doc'}

# CORS настройки
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001", 
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "https://localhost",
    "https://127.0.0.1"
]

# Добавляем production домены из переменных окружения
PRODUCTION_DOMAINS = os.getenv("PRODUCTION_DOMAINS", "").split(",")
if PRODUCTION_DOMAINS and PRODUCTION_DOMAINS[0]:
    CORS_ORIGINS.extend([domain.strip() for domain in PRODUCTION_DOMAINS if domain.strip()])

# Добавляем DigitalOcean домены
DIGITALOCEAN_DOMAINS = os.getenv("DIGITALOCEAN_DOMAINS", "").split(",")
if DIGITALOCEAN_DOMAINS and DIGITALOCEAN_DOMAINS[0]:
    CORS_ORIGINS.extend([domain.strip() for domain in DIGITALOCEAN_DOMAINS if domain.strip()])

# Добавляем общие домены для разработки
CORS_ORIGINS.extend([
    "http://localhost:3000",
    "https://localhost:3000",
    "http://127.0.0.1:3000",
    "https://127.0.0.1:3000"
]) 