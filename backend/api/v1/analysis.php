<?php
/**
 * API эндпоинт для анализа CV
 * Использует Mistral AI для анализа резюме кандидатов
 */

require_once '../../config/config.php';
require_once '../../config/supabase.php';
require_once '../../config/mistral.php';

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

// Инициализация клиентов
$supabase = new SupabaseClient();
$mistral = new MistralClient();

try {
    $method = $_SERVER['REQUEST_METHOD'];
    $path = $_GET['action'] ?? '';
    
    switch ($method) {
        case 'POST':
            $input = json_decode(file_get_contents('php://input'), true);
            
            switch ($path) {
                case 'cv':
                    handleCVAnalysis($supabase, $mistral, $input);
                    break;
                    
                case 'compare':
                    handleCandidateComparison($supabase, $mistral, $input);
                    break;
                    
                case 'questions':
                    handleInterviewQuestions($supabase, $mistral, $input);
                    break;
                    
                default:
                    http_response_code(404);
                    echo json_encode(['error' => 'Endpoint not found']);
                    break;
            }
            break;
            
        case 'GET':
            switch ($path) {
                case 'history':
                    handleGetAnalysisHistory($supabase);
                    break;
                    
                case 'detail':
                    handleGetAnalysisDetail($supabase);
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
    logMessage("Analysis API Error: " . $e->getMessage(), 'ERROR');
    http_response_code(500);
    echo json_encode(['error' => 'Internal server error']);
}

/**
 * Обработка анализа CV
 */
function handleCVAnalysis($supabase, $mistral, $input) {
    // Проверка аутентификации
    $user = getAuthenticatedUser($supabase);
    if (!$user) {
        http_response_code(401);
        echo json_encode(['error' => 'Authentication required']);
        return;
    }
    
    // Валидация входных данных
    if (!isset($input['cv_content']) || empty($input['cv_content'])) {
        http_response_code(400);
        echo json_encode(['error' => 'CV content is required']);
        return;
    }
    
    $cvContent = $input['cv_content'];
    $jobDescription = $input['job_description'] ?? null;
    $candidateName = $input['candidate_name'] ?? 'Unknown';
    $candidateEmail = $input['candidate_email'] ?? null;
    
    // Ограничение размера CV
    if (strlen($cvContent) > 50000) {
        http_response_code(400);
        echo json_encode(['error' => 'CV content is too large (max 50KB)']);
        return;
    }
    
    try {
        // Анализ CV с помощью Mistral AI
        $startTime = microtime(true);
        $analysis = $mistral->analyzeCV($cvContent, $jobDescription);
        $processingTime = round((microtime(true) - $startTime) * 1000, 2);
        
        if (!$analysis['success']) {
            http_response_code(500);
            echo json_encode(['error' => 'CV analysis failed: ' . $analysis['error']]);
            return;
        }
        
        // Сохранение результатов анализа в базу данных
        $analysisData = [
            'user_id' => $user['id'],
            'candidate_name' => $candidateName,
            'candidate_email' => $candidateEmail,
            'cv_content' => $cvContent,
            'job_description' => $jobDescription,
            'analysis_result' => json_encode($analysis['analysis']),
            'overall_score' => $analysis['analysis']['overall_score'] ?? 0,
            'processing_time_ms' => $processingTime,
            'created_at' => date('Y-m-d H:i:s')
        ];
        
        $result = $supabase->insert('cv_analyses', $analysisData, true);
        
        if (isset($result['error'])) {
            logMessage("Failed to save analysis: " . json_encode($result['error']), 'ERROR');
        }
        
        logMessage("CV analysis completed for user: " . $user['email'], 'INFO');
        
        echo json_encode([
            'success' => true,
            'message' => 'CV analysis completed successfully',
            'analysis' => $analysis['analysis'],
            'processing_time_ms' => $processingTime,
            'analysis_id' => $result['id'] ?? null
        ]);
        
    } catch (Exception $e) {
        logMessage("CV analysis error: " . $e->getMessage(), 'ERROR');
        http_response_code(500);
        echo json_encode(['error' => 'CV analysis failed']);
    }
}

/**
 * Обработка сравнения кандидатов
 */
function handleCandidateComparison($supabase, $mistral, $input) {
    // Проверка аутентификации
    $user = getAuthenticatedUser($supabase);
    if (!$user) {
        http_response_code(401);
        echo json_encode(['error' => 'Authentication required']);
        return;
    }
    
    // Валидация входных данных
    if (!isset($input['candidates']) || !is_array($input['candidates']) || count($input['candidates']) < 2) {
        http_response_code(400);
        echo json_encode(['error' => 'At least 2 candidates are required']);
        return;
    }
    
    $candidates = $input['candidates'];
    $jobDescription = $input['job_description'] ?? null;
    
    // Валидация кандидатов
    foreach ($candidates as $candidate) {
        if (!isset($candidate['cv_content']) || empty($candidate['cv_content'])) {
            http_response_code(400);
            echo json_encode(['error' => 'CV content is required for all candidates']);
            return;
        }
    }
    
    try {
        // Сравнение кандидатов с помощью Mistral AI
        $startTime = microtime(true);
        $comparison = $mistral->compareCandidates($candidates, $jobDescription);
        $processingTime = round((microtime(true) - $startTime) * 1000, 2);
        
        if (!$comparison['success']) {
            http_response_code(500);
            echo json_encode(['error' => 'Candidate comparison failed: ' . $comparison['error']]);
            return;
        }
        
        // Сохранение результатов сравнения
        $comparisonData = [
            'user_id' => $user['id'],
            'job_description' => $jobDescription,
            'candidates_count' => count($candidates),
            'comparison_result' => json_encode($comparison['comparison']),
            'processing_time_ms' => $processingTime,
            'created_at' => date('Y-m-d H:i:s')
        ];
        
        $result = $supabase->insert('candidate_comparisons', $comparisonData, true);
        
        logMessage("Candidate comparison completed for user: " . $user['email'], 'INFO');
        
        echo json_encode([
            'success' => true,
            'message' => 'Candidate comparison completed successfully',
            'comparison' => $comparison['comparison'],
            'processing_time_ms' => $processingTime,
            'comparison_id' => $result['id'] ?? null
        ]);
        
    } catch (Exception $e) {
        logMessage("Candidate comparison error: " . $e->getMessage(), 'ERROR');
        http_response_code(500);
        echo json_encode(['error' => 'Candidate comparison failed']);
    }
}

/**
 * Генерация вопросов для интервью
 */
function handleInterviewQuestions($supabase, $mistral, $input) {
    // Проверка аутентификации
    $user = getAuthenticatedUser($supabase);
    if (!$user) {
        http_response_code(401);
        echo json_encode(['error' => 'Authentication required']);
        return;
    }
    
    // Валидация входных данных
    if (!isset($input['cv_content']) || empty($input['cv_content'])) {
        http_response_code(400);
        echo json_encode(['error' => 'CV content is required']);
        return;
    }
    
    $cvContent = $input['cv_content'];
    $jobDescription = $input['job_description'] ?? null;
    
    try {
        // Генерация вопросов с помощью Mistral AI
        $startTime = microtime(true);
        $questions = $mistral->generateInterviewQuestions($cvContent, $jobDescription);
        $processingTime = round((microtime(true) - $startTime) * 1000, 2);
        
        if (!$questions['success']) {
            http_response_code(500);
            echo json_encode(['error' => 'Questions generation failed: ' . $questions['error']]);
            return;
        }
        
        logMessage("Interview questions generated for user: " . $user['email'], 'INFO');
        
        echo json_encode([
            'success' => true,
            'message' => 'Interview questions generated successfully',
            'questions' => $questions['questions'],
            'processing_time_ms' => $processingTime
        ]);
        
    } catch (Exception $e) {
        logMessage("Interview questions error: " . $e->getMessage(), 'ERROR');
        http_response_code(500);
        echo json_encode(['error' => 'Questions generation failed']);
    }
}

/**
 * Получение истории анализов
 */
function handleGetAnalysisHistory($supabase) {
    // Проверка аутентификации
    $user = getAuthenticatedUser($supabase);
    if (!$user) {
        http_response_code(401);
        echo json_encode(['error' => 'Authentication required']);
        return;
    }
    
    try {
        // Получение истории анализов пользователя
        $analyses = $supabase->select('cv_analyses', [
            'user_id' => 'eq.' . $user['id']
        ], true);
        
        // Форматирование данных
        $formattedAnalyses = [];
        foreach ($analyses as $analysis) {
            $formattedAnalyses[] = [
                'id' => $analysis['id'],
                'candidate_name' => $analysis['candidate_name'],
                'candidate_email' => $analysis['candidate_email'],
                'overall_score' => $analysis['overall_score'],
                'processing_time_ms' => $analysis['processing_time_ms'],
                'created_at' => $analysis['created_at']
            ];
        }
        
        echo json_encode([
            'success' => true,
            'analyses' => $formattedAnalyses
        ]);
        
    } catch (Exception $e) {
        logMessage("Get analysis history error: " . $e->getMessage(), 'ERROR');
        http_response_code(500);
        echo json_encode(['error' => 'Failed to get analysis history']);
    }
}

/**
 * Получение деталей анализа
 */
function handleGetAnalysisDetail($supabase) {
    // Проверка аутентификации
    $user = getAuthenticatedUser($supabase);
    if (!$user) {
        http_response_code(401);
        echo json_encode(['error' => 'Authentication required']);
        return;
    }
    
    $analysisId = $_GET['id'] ?? null;
    if (!$analysisId) {
        http_response_code(400);
        echo json_encode(['error' => 'Analysis ID is required']);
        return;
    }
    
    try {
        // Получение деталей анализа
        $analyses = $supabase->select('cv_analyses', [
            'id' => 'eq.' . $analysisId,
            'user_id' => 'eq.' . $user['id']
        ], true);
        
        if (empty($analyses)) {
            http_response_code(404);
            echo json_encode(['error' => 'Analysis not found']);
            return;
        }
        
        $analysis = $analyses[0];
        $analysisResult = json_decode($analysis['analysis_result'], true);
        
        echo json_encode([
            'success' => true,
            'analysis' => [
                'id' => $analysis['id'],
                'candidate_name' => $analysis['candidate_name'],
                'candidate_email' => $analysis['candidate_email'],
                'cv_content' => $analysis['cv_content'],
                'job_description' => $analysis['job_description'],
                'analysis_result' => $analysisResult,
                'overall_score' => $analysis['overall_score'],
                'processing_time_ms' => $analysis['processing_time_ms'],
                'created_at' => $analysis['created_at']
            ]
        ]);
        
    } catch (Exception $e) {
        logMessage("Get analysis detail error: " . $e->getMessage(), 'ERROR');
        http_response_code(500);
        echo json_encode(['error' => 'Failed to get analysis details']);
    }
}

/**
 * Получение аутентифицированного пользователя
 */
function getAuthenticatedUser($supabase) {
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
        return null;
    }
    
    try {
        $user = $supabase->getUser($accessToken);
        
        if (isset($user['error'])) {
            return null;
        }
        
        return $user;
        
    } catch (Exception $e) {
        logMessage("Authentication error: " . $e->getMessage(), 'ERROR');
        return null;
    }
}
?> 