<?php
/**
 * API эндпоинт для аутентификации
 * Обрабатывает регистрацию, вход и выход пользователей
 */

require_once '../../config/config.php';
require_once '../../config/supabase.php';

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

// Инициализация Supabase клиента
$supabase = new SupabaseClient();

try {
    $method = $_SERVER['REQUEST_METHOD'];
    $path = $_GET['action'] ?? '';
    
    switch ($method) {
        case 'POST':
            $input = json_decode(file_get_contents('php://input'), true);
            
            switch ($path) {
                case 'register':
                    handleRegister($supabase, $input);
                    break;
                    
                case 'login':
                    handleLogin($supabase, $input);
                    break;
                    
                case 'logout':
                    handleLogout($supabase, $input);
                    break;
                    
                default:
                    http_response_code(404);
                    echo json_encode(['error' => 'Endpoint not found']);
                    break;
            }
            break;
            
        case 'GET':
            switch ($path) {
                case 'profile':
                    handleGetProfile($supabase);
                    break;
                    
                default:
                    http_response_code(404);
                    echo json_encode(['error' => 'Endpoint not found']);
                    break;
            }
            break;
            
        case 'PUT':
            $input = json_decode(file_get_contents('php://input'), true);
            
            switch ($path) {
                case 'profile':
                    handleUpdateProfile($supabase, $input);
                    break;
                    
                default:
                    http_response_code(404);
                    echo json_encode(['error' => 'Endpoint not found']);
                    break;
            }
            break;
            
        default:
            http_response_code(405);
            echo json_encode(['error' => 'Method not allowed']);
            break;
    }
    
} catch (Exception $e) {
    logMessage("Auth API Error: " . $e->getMessage(), 'ERROR');
    http_response_code(500);
    echo json_encode(['error' => 'Internal server error']);
}

/**
 * Обработка регистрации пользователя
 */
function handleRegister($supabase, $input) {
    // Валидация входных данных
    if (!isset($input['email']) || !isset($input['password'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Email and password are required']);
        return;
    }
    
    $email = filter_var($input['email'], FILTER_VALIDATE_EMAIL);
    if (!$email) {
        http_response_code(400);
        echo json_encode(['error' => 'Invalid email format']);
        return;
    }
    
    $password = $input['password'];
    if (strlen($password) < 6) {
        http_response_code(400);
        echo json_encode(['error' => 'Password must be at least 6 characters']);
        return;
    }
    
    // Дополнительные данные пользователя
    $userData = [
        'full_name' => $input['full_name'] ?? '',
        'company' => $input['company'] ?? '',
        'role' => $input['role'] ?? 'user'
    ];
    
    try {
        $result = $supabase->signUp($email, $password, $userData);
        
        if (isset($result['error'])) {
            http_response_code(400);
            echo json_encode(['error' => $result['error']]);
            return;
        }
        
        // Сохранение дополнительной информации в профиль
        if (isset($result['user']['id'])) {
            $profileData = [
                'id' => $result['user']['id'],
                'email' => $email,
                'full_name' => $userData['full_name'],
                'company' => $userData['company'],
                'role' => $userData['role'],
                'created_at' => date('Y-m-d H:i:s'),
                'updated_at' => date('Y-m-d H:i:s')
            ];
            
            $supabase->insert('profiles', $profileData, true);
        }
        
        logMessage("User registered: $email", 'INFO');
        
        echo json_encode([
            'success' => true,
            'message' => 'Registration successful',
            'user' => $result['user'] ?? null
        ]);
        
    } catch (Exception $e) {
        logMessage("Registration error: " . $e->getMessage(), 'ERROR');
        http_response_code(500);
        echo json_encode(['error' => 'Registration failed']);
    }
}

/**
 * Обработка входа пользователя
 */
function handleLogin($supabase, $input) {
    // Валидация входных данных
    if (!isset($input['email']) || !isset($input['password'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Email and password are required']);
        return;
    }
    
    $email = filter_var($input['email'], FILTER_VALIDATE_EMAIL);
    if (!$email) {
        http_response_code(400);
        echo json_encode(['error' => 'Invalid email format']);
        return;
    }
    
    try {
        $result = $supabase->auth($email, $input['password']);
        
        if (isset($result['error'])) {
            http_response_code(401);
            echo json_encode(['error' => 'Invalid credentials']);
            return;
        }
        
        // Получение профиля пользователя
        $userProfile = null;
        if (isset($result['user']['id'])) {
            $profiles = $supabase->select('profiles', ['id' => 'eq.' . $result['user']['id']], true);
            if (!empty($profiles)) {
                $userProfile = $profiles[0];
            }
        }
        
        logMessage("User logged in: $email", 'INFO');
        
        echo json_encode([
            'success' => true,
            'message' => 'Login successful',
            'access_token' => $result['access_token'] ?? null,
            'refresh_token' => $result['refresh_token'] ?? null,
            'user' => $result['user'] ?? null,
            'profile' => $userProfile
        ]);
        
    } catch (Exception $e) {
        logMessage("Login error: " . $e->getMessage(), 'ERROR');
        http_response_code(500);
        echo json_encode(['error' => 'Login failed']);
    }
}

/**
 * Обработка выхода пользователя
 */
function handleLogout($supabase, $input) {
    $accessToken = $input['access_token'] ?? null;
    
    if (!$accessToken) {
        http_response_code(400);
        echo json_encode(['error' => 'Access token is required']);
        return;
    }
    
    try {
        $result = $supabase->signOut($accessToken);
        
        logMessage("User logged out", 'INFO');
        
        echo json_encode([
            'success' => true,
            'message' => 'Logout successful'
        ]);
        
    } catch (Exception $e) {
        logMessage("Logout error: " . $e->getMessage(), 'ERROR');
        http_response_code(500);
        echo json_encode(['error' => 'Logout failed']);
    }
}

/**
 * Получение профиля пользователя
 */
function handleGetProfile($supabase) {
    $headers = getallheaders();
    $accessToken = null;
    
    // Извлечение токена из заголовка Authorization
    if (isset($headers['Authorization'])) {
        $authHeader = $headers['Authorization'];
        if (strpos($authHeader, 'Bearer ') === 0) {
            $accessToken = substr($authHeader, 7);
        }
    }
    
    if (!$accessToken) {
        http_response_code(401);
        echo json_encode(['error' => 'Access token is required']);
        return;
    }
    
    try {
        $user = $supabase->getUser($accessToken);
        
        if (isset($user['error'])) {
            http_response_code(401);
            echo json_encode(['error' => 'Invalid token']);
            return;
        }
        
        // Получение профиля пользователя
        $userProfile = null;
        if (isset($user['id'])) {
            $profiles = $supabase->select('profiles', ['id' => 'eq.' . $user['id']], true);
            if (!empty($profiles)) {
                $userProfile = $profiles[0];
            }
        }
        
        echo json_encode([
            'success' => true,
            'user' => $user,
            'profile' => $userProfile
        ]);
        
    } catch (Exception $e) {
        logMessage("Get profile error: " . $e->getMessage(), 'ERROR');
        http_response_code(500);
        echo json_encode(['error' => 'Failed to get profile']);
    }
}

/**
 * Обновление профиля пользователя
 */
function handleUpdateProfile($supabase, $input) {
    $headers = getallheaders();
    $accessToken = null;
    
    // Извлечение токена из заголовка Authorization
    if (isset($headers['Authorization'])) {
        $authHeader = $headers['Authorization'];
        if (strpos($authHeader, 'Bearer ') === 0) {
            $accessToken = substr($authHeader, 7);
        }
    }
    
    if (!$accessToken) {
        http_response_code(401);
        echo json_encode(['error' => 'Access token is required']);
        return;
    }
    
    try {
        $user = $supabase->getUser($accessToken);
        
        if (isset($user['error'])) {
            http_response_code(401);
            echo json_encode(['error' => 'Invalid token']);
            return;
        }
        
        // Обновление данных пользователя в Supabase Auth
        $userData = [];
        if (isset($input['full_name'])) {
            $userData['user_metadata'] = ['full_name' => $input['full_name']];
        }
        
        if (!empty($userData)) {
            $supabase->updateUser($accessToken, $userData);
        }
        
        // Обновление профиля в базе данных
        $profileData = [
            'updated_at' => date('Y-m-d H:i:s')
        ];
        
        if (isset($input['full_name'])) {
            $profileData['full_name'] = $input['full_name'];
        }
        if (isset($input['company'])) {
            $profileData['company'] = $input['company'];
        }
        if (isset($input['role'])) {
            $profileData['role'] = $input['role'];
        }
        
        $supabase->update('profiles', $profileData, ['id' => 'eq.' . $user['id']], true);
        
        logMessage("Profile updated for user: " . $user['email'], 'INFO');
        
        echo json_encode([
            'success' => true,
            'message' => 'Profile updated successfully'
        ]);
        
    } catch (Exception $e) {
        logMessage("Update profile error: " . $e->getMessage(), 'ERROR');
        http_response_code(500);
        echo json_encode(['error' => 'Failed to update profile']);
    }
}
?> 