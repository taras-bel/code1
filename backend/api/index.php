<?php
/**
 * Главный файл API
 * Обрабатывает все API запросы и направляет их к соответствующим обработчикам
 */

require_once '../config/config.php';

// Настройка CORS
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With');

// Обработка preflight запросов
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Получение пути запроса
$requestUri = $_SERVER['REQUEST_URI'];
$basePath = '/api/';

// Удаление базового пути из URI
$path = str_replace($basePath, '', $requestUri);

// Удаление query параметров
$path = strtok($path, '?');

// Разделение пути на части
$pathParts = explode('/', trim($path, '/'));

// Определение версии API и ресурса
$version = $pathParts[0] ?? 'v1';
$resource = $pathParts[1] ?? '';
$action = $pathParts[2] ?? '';

// Проверка версии API
if ($version !== 'v1') {
    http_response_code(400);
    echo json_encode(['error' => 'Unsupported API version']);
    exit();
}

// Маршрутизация запросов
try {
    switch ($resource) {
        case 'auth':
            // Перенаправление к auth.php
            $_GET['action'] = $action;
            include "v1/auth.php";
            break;
            
        case 'analysis':
            // Перенаправление к analysis.php
            $_GET['action'] = $action;
            include "v1/analysis.php";
            break;
            
        case 'users':
            // Перенаправление к users.php
            $_GET['action'] = $action;
            include "v1/users.php";
            break;
            
        case 'files':
            // Перенаправление к files.php
            $_GET['action'] = $action;
            include "v1/files.php";
            break;
            
        case 'health':
            // Проверка здоровья API
            handleHealthCheck();
            break;
            
        default:
            http_response_code(404);
            echo json_encode(['error' => 'Resource not found']);
            break;
    }
    
} catch (Exception $e) {
    logMessage("API Error: " . $e->getMessage(), 'ERROR');
    http_response_code(500);
    echo json_encode(['error' => 'Internal server error']);
}

/**
 * Проверка здоровья API
 */
function handleHealthCheck() {
    $health = [
        'status' => 'healthy',
        'timestamp' => date('Y-m-d H:i:s'),
        'version' => '1.0.0',
        'services' => [
            'api' => 'ok',
            'database' => 'unknown',
            'mistral_ai' => 'unknown'
        ]
    ];
    
    // Проверка подключения к Supabase
    try {
        require_once '../config/supabase.php';
        $supabase = new SupabaseClient();
        
        // Простой тест подключения
        $testResult = $supabase->select('profiles', ['limit' => '1'], true);
        $health['services']['database'] = 'ok';
        
    } catch (Exception $e) {
        $health['services']['database'] = 'error';
        $health['database_error'] = $e->getMessage();
    }
    
    // Проверка подключения к Mistral AI
    try {
        require_once '../config/mistral.php';
        $mistral = new MistralClient();
        
        // Простой тест подключения
        $models = $mistral->getModels();
        if (isset($models['data'])) {
            $health['services']['mistral_ai'] = 'ok';
        } else {
            $health['services']['mistral_ai'] = 'error';
        }
        
    } catch (Exception $e) {
        $health['services']['mistral_ai'] = 'error';
        $health['mistral_error'] = $e->getMessage();
    }
    
    // Определение общего статуса
    if (in_array('error', $health['services'])) {
        $health['status'] = 'degraded';
    }
    
    echo json_encode($health);
}

/**
 * Логирование API запросов
 */
function logApiRequest($method, $path, $statusCode, $responseTime = null) {
    $logData = [
        'timestamp' => date('Y-m-d H:i:s'),
        'method' => $method,
        'path' => $path,
        'status_code' => $statusCode,
        'ip' => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
        'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? 'unknown'
    ];
    
    if ($responseTime) {
        $logData['response_time_ms'] = $responseTime;
    }
    
    logMessage("API Request: " . json_encode($logData), 'INFO');
}

// Логирование запроса при завершении
register_shutdown_function(function() use ($requestUri) {
    $statusCode = http_response_code();
    logApiRequest($_SERVER['REQUEST_METHOD'], $requestUri, $statusCode);
});
?> 