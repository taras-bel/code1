<?php
/**
 * Основная конфигурация приложения
 * NoaMetrics - PHP Backend Configuration
 */

// Включение отображения ошибок для разработки
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Настройки часового пояса
date_default_timezone_set('UTC');

// Конфигурация Supabase
define('SUPABASE_URL', 'https://your-project.supabase.co');
define('SUPABASE_ANON_KEY', 'your-anon-key');
define('SUPABASE_SERVICE_ROLE_KEY', 'your-service-role-key');

// Конфигурация Mistral AI
define('MISTRAL_API_KEY', 'your-mistral-api-key');
define('MISTRAL_API_URL', 'https://api.mistral.ai/v1');

// Настройки безопасности
define('SECRET_KEY', 'your-secret-key-here-make-it-long-and-random');
define('JWT_SECRET', 'your-jwt-secret-key');

// Настройки CORS
define('ALLOWED_ORIGINS', [
    'http://localhost:3000',
    'http://localhost:3001',
    'https://noametrics.com',
    'https://www.noametrics.com'
]);

// Настройки загрузки файлов
define('MAX_FILE_SIZE', 10 * 1024 * 1024); // 10MB
define('ALLOWED_FILE_TYPES', [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain'
]);

// Настройки кэширования
define('CACHE_ENABLED', true);
define('CACHE_DURATION', 3600); // 1 час

// Настройки логирования
define('LOG_ENABLED', true);
define('LOG_FILE', __DIR__ . '/../logs/app.log');

// Настройки базы данных (если используется локальная БД)
define('DB_HOST', 'localhost');
define('DB_NAME', 'noametrics');
define('DB_USER', 'root');
define('DB_PASS', '');

// Функция для получения конфигурации
function getConfig($key, $default = null) {
    $config = [
        'supabase_url' => SUPABASE_URL,
        'supabase_anon_key' => SUPABASE_ANON_KEY,
        'supabase_service_role_key' => SUPABASE_SERVICE_ROLE_KEY,
        'mistral_api_key' => MISTRAL_API_KEY,
        'mistral_api_url' => MISTRAL_API_URL,
        'secret_key' => SECRET_KEY,
        'jwt_secret' => JWT_SECRET,
        'allowed_origins' => ALLOWED_ORIGINS,
        'max_file_size' => MAX_FILE_SIZE,
        'allowed_file_types' => ALLOWED_FILE_TYPES,
        'cache_enabled' => CACHE_ENABLED,
        'cache_duration' => CACHE_DURATION,
        'log_enabled' => LOG_ENABLED,
        'log_file' => LOG_FILE
    ];
    
    return $config[$key] ?? $default;
}

// Функция для проверки окружения
function isDevelopment() {
    return $_SERVER['HTTP_HOST'] === 'localhost' || 
           strpos($_SERVER['HTTP_HOST'], '127.0.0.1') !== false;
}

// Функция для логирования
function logMessage($message, $level = 'INFO') {
    if (!LOG_ENABLED) return;
    
    $logDir = dirname(LOG_FILE);
    if (!is_dir($logDir)) {
        mkdir($logDir, 0755, true);
    }
    
    $timestamp = date('Y-m-d H:i:s');
    $logEntry = "[$timestamp] [$level] $message" . PHP_EOL;
    
    file_put_contents(LOG_FILE, $logEntry, FILE_APPEND | LOCK_EX);
}

// Функция для валидации API ключей
function validateApiKeys() {
    $requiredKeys = [
        'SUPABASE_URL' => SUPABASE_URL,
        'SUPABASE_ANON_KEY' => SUPABASE_ANON_KEY,
        'SUPABASE_SERVICE_ROLE_KEY' => SUPABASE_SERVICE_ROLE_KEY,
        'MISTRAL_API_KEY' => MISTRAL_API_KEY
    ];
    
    $missingKeys = [];
    foreach ($requiredKeys as $key => $value) {
        if (empty($value) || $value === 'your-' . strtolower($key)) {
            $missingKeys[] = $key;
        }
    }
    
    if (!empty($missingKeys)) {
        logMessage('Missing API keys: ' . implode(', ', $missingKeys), 'ERROR');
        return false;
    }
    
    return true;
}

// Инициализация конфигурации
if (isDevelopment()) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
} else {
    error_reporting(0);
    ini_set('display_errors', 0);
}

// Проверка API ключей при загрузке
if (!validateApiKeys()) {
    logMessage('API keys validation failed', 'ERROR');
}
?> 