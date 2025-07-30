<?php
/**
 * Mistral AI Client для PHP
 * Обеспечивает взаимодействие с Mistral AI API для анализа CV
 */

require_once __DIR__ . '/config.php';

class MistralClient {
    private $apiKey;
    private $apiUrl;
    private $model;
    
    public function __construct($apiKey = null, $apiUrl = null) {
        $this->apiKey = $apiKey ?: MISTRAL_API_KEY;
        $this->apiUrl = $apiUrl ?: MISTRAL_API_URL;
        $this->model = 'mistral-large-latest';
    }
    
    /**
     * Выполнение запроса к Mistral AI API
     */
    private function makeRequest($endpoint, $data) {
        $headers = [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $this->apiKey
        ];
        
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->apiUrl . $endpoint);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($ch, CURLOPT_TIMEOUT, 60);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        curl_close($ch);
        
        if ($error) {
            logMessage("Mistral CURL Error: $error", 'ERROR');
            throw new Exception("Mistral CURL Error: $error");
        }
        
        $result = json_decode($response, true);
        
        if ($httpCode >= 400) {
            logMessage("Mistral API Error: HTTP $httpCode - " . json_encode($result), 'ERROR');
            throw new Exception("Mistral API Error: " . ($result['error']['message'] ?? 'Unknown error'));
        }
        
        return $result;
    }
    
    /**
     * Отправка сообщения в чат
     */
    public function chat($messages, $temperature = 0.7, $maxTokens = 4000) {
        $data = [
            'model' => $this->model,
            'messages' => $messages,
            'temperature' => $temperature,
            'max_tokens' => $maxTokens
        ];
        
        return $this->makeRequest('/chat/completions', $data);
    }
    
    /**
     * Анализ CV
     */
    public function analyzeCV($cvContent, $jobDescription = null) {
        $systemPrompt = "Ты эксперт по анализу резюме и подбору персонала. Твоя задача - проанализировать резюме кандидата и предоставить детальную оценку.";
        
        $userPrompt = "Проанализируй следующее резюме:\n\n$cvContent";
        
        if ($jobDescription) {
            $userPrompt .= "\n\nВ контексте следующего описания вакансии:\n$jobDescription";
        }
        
        $userPrompt .= "\n\nПредоставь анализ в следующем JSON формате:\n";
        $userPrompt .= "{\n";
        $userPrompt .= "  \"overall_score\": 85,\n";
        $userPrompt .= "  \"skills_analysis\": {\n";
        $userPrompt .= "    \"technical_skills\": [\"PHP\", \"JavaScript\", \"MySQL\"],\n";
        $userPrompt .= "    \"soft_skills\": [\"Коммуникация\", \"Лидерство\"],\n";
        $userPrompt .= "    \"missing_skills\": [\"Docker\", \"Kubernetes\"]\n";
        $userPrompt .= "  },\n";
        $userPrompt .= "  \"experience_evaluation\": {\n";
        $userPrompt .= "    \"years_of_experience\": 5,\n";
        $userPrompt .= "    \"relevant_experience\": \"Высокая\",\n";
        $userPrompt .= "    \"key_achievements\": [\"Успешно реализовал 10+ проектов\"]\n";
        $userPrompt .= "  },\n";
        $userPrompt .= "  \"education_assessment\": {\n";
        $userPrompt .= "    \"level\": \"Высшее\",\n";
        $userPrompt .= "    \"relevance\": \"Высокая\",\n";
        $userPrompt .= "    \"certifications\": [\"AWS Certified Developer\"]\n";
        $userPrompt .= "  },\n";
        $userPrompt .= "  \"recommendations\": {\n";
        $userPrompt .= "    \"hire_recommendation\": \"Рекомендую\",\n";
        $userPrompt .= "    \"strengths\": [\"Сильные технические навыки\"],\n";
        $userPrompt .= "    \"weaknesses\": [\"Недостаточно опыта в DevOps\"],\n";
        $userPrompt .= "    \"improvement_suggestions\": [\"Изучить Docker и Kubernetes\"]\n";
        $userPrompt .= "  },\n";
        $userPrompt .= "  \"detailed_analysis\": \"Подробный текстовый анализ...\"\n";
        $userPrompt .= "}";
        
        $messages = [
            [
                'role' => 'system',
                'content' => $systemPrompt
            ],
            [
                'role' => 'user',
                'content' => $userPrompt
            ]
        ];
        
        try {
            $response = $this->chat($messages, 0.3, 6000);
            $analysis = json_decode($response['choices'][0]['message']['content'], true);
            
            if (json_last_error() !== JSON_ERROR_NONE) {
                // Если JSON невалидный, возвращаем текстовый анализ
                return [
                    'success' => true,
                    'analysis' => [
                        'overall_score' => 75,
                        'detailed_analysis' => $response['choices'][0]['message']['content'],
                        'raw_response' => $response['choices'][0]['message']['content']
                    ]
                ];
            }
            
            return [
                'success' => true,
                'analysis' => $analysis
            ];
            
        } catch (Exception $e) {
            logMessage("CV Analysis Error: " . $e->getMessage(), 'ERROR');
            return [
                'success' => false,
                'error' => $e->getMessage()
            ];
        }
    }
    
    /**
     * Сравнение кандидатов
     */
    public function compareCandidates($candidates, $jobDescription) {
        $systemPrompt = "Ты эксперт по подбору персонала. Сравни кандидатов и предоставь рейтинг.";
        
        $userPrompt = "Сравни следующих кандидатов для вакансии:\n\n";
        $userPrompt .= "Описание вакансии:\n$jobDescription\n\n";
        
        foreach ($candidates as $index => $candidate) {
            $userPrompt .= "Кандидат " . ($index + 1) . ":\n";
            $userPrompt .= "CV: " . $candidate['cv_content'] . "\n\n";
        }
        
        $userPrompt .= "Предоставь сравнение в JSON формате:\n";
        $userPrompt .= "{\n";
        $userPrompt .= "  \"comparison\": [\n";
        $userPrompt .= "    {\n";
        $userPrompt .= "      \"candidate_id\": 1,\n";
        $userPrompt .= "      \"score\": 85,\n";
        $userPrompt .= "      \"rank\": 1,\n";
        $userPrompt .= "      \"strengths\": [\"Сильные технические навыки\"],\n";
        $userPrompt .= "      \"weaknesses\": [\"Недостаточно опыта\"],\n";
        $userPrompt .= "      \"recommendation\": \"Рекомендую\"\n";
        $userPrompt .= "    }\n";
        $userPrompt .= "  ],\n";
        $userPrompt .= "  \"summary\": \"Общий анализ сравнения...\"\n";
        $userPrompt .= "}";
        
        $messages = [
            [
                'role' => 'system',
                'content' => $systemPrompt
            ],
            [
                'role' => 'user',
                'content' => $userPrompt
            ]
        ];
        
        try {
            $response = $this->chat($messages, 0.3, 8000);
            $comparison = json_decode($response['choices'][0]['message']['content'], true);
            
            return [
                'success' => true,
                'comparison' => $comparison
            ];
            
        } catch (Exception $e) {
            logMessage("Candidate Comparison Error: " . $e->getMessage(), 'ERROR');
            return [
                'success' => false,
                'error' => $e->getMessage()
            ];
        }
    }
    
    /**
     * Генерация вопросов для интервью
     */
    public function generateInterviewQuestions($cvContent, $jobDescription) {
        $systemPrompt = "Ты HR-специалист. Создай вопросы для технического интервью на основе резюме кандидата.";
        
        $userPrompt = "Создай вопросы для интервью кандидата:\n\n";
        $userPrompt .= "Резюме:\n$cvContent\n\n";
        $userPrompt .= "Вакансия:\n$jobDescription\n\n";
        $userPrompt .= "Предоставь вопросы в JSON формате:\n";
        $userPrompt .= "{\n";
        $userPrompt .= "  \"technical_questions\": [\n";
        $userPrompt .= "    {\n";
        $userPrompt .= "      \"question\": \"Расскажите о вашем опыте работы с PHP?\",\n";
        $userPrompt .= "      \"category\": \"Programming\",\n";
        $userPrompt .= "      \"difficulty\": \"Intermediate\"\n";
        $userPrompt .= "    }\n";
        $userPrompt .= "  ],\n";
        $userPrompt .= "  \"behavioral_questions\": [\n";
        $userPrompt .= "    {\n";
        $userPrompt .= "      \"question\": \"Опишите сложный проект, который вы реализовали\",\n";
        $userPrompt .= "      \"category\": \"Leadership\"\n";
        $userPrompt .= "    }\n";
        $userPrompt .= "  ],\n";
        $userPrompt .= "  \"red_flags\": [\n";
        $userPrompt .= "    \"Обратите внимание на отсутствие опыта в DevOps\"\n";
        $userPrompt .= "  ]\n";
        $userPrompt .= "}";
        
        $messages = [
            [
                'role' => 'system',
                'content' => $systemPrompt
            ],
            [
                'role' => 'user',
                'content' => $userPrompt
            ]
        ];
        
        try {
            $response = $this->chat($messages, 0.5, 4000);
            $questions = json_decode($response['choices'][0]['message']['content'], true);
            
            return [
                'success' => true,
                'questions' => $questions
            ];
            
        } catch (Exception $e) {
            logMessage("Interview Questions Error: " . $e->getMessage(), 'ERROR');
            return [
                'success' => false,
                'error' => $e->getMessage()
            ];
        }
    }
    
    /**
     * Установка модели
     */
    public function setModel($model) {
        $this->model = $model;
    }
    
    /**
     * Получение доступных моделей
     */
    public function getModels() {
        $headers = [
            'Authorization: Bearer ' . $this->apiKey
        ];
        
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->apiUrl . '/models');
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        return json_decode($response, true);
    }
}
?> 