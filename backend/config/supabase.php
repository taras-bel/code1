<?php
/**
 * Supabase Client для PHP
 * Обеспечивает взаимодействие с Supabase API
 */

require_once __DIR__ . '/config.php';

class SupabaseClient {
    private $url;
    private $anonKey;
    private $serviceRoleKey;
    private $headers;
    
    public function __construct($url = null, $anonKey = null, $serviceRoleKey = null) {
        $this->url = $url ?: SUPABASE_URL;
        $this->anonKey = $anonKey ?: SUPABASE_ANON_KEY;
        $this->serviceRoleKey = $serviceRoleKey ?: SUPABASE_SERVICE_ROLE_KEY;
        
        $this->headers = [
            'Content-Type: application/json',
            'apikey: ' . $this->anonKey,
            'Authorization: Bearer ' . $this->anonKey
        ];
    }
    
    /**
     * Выполнение HTTP запроса
     */
    private function makeRequest($endpoint, $method = 'GET', $data = null, $useServiceRole = false) {
        $url = $this->url . $endpoint;
        
        $headers = $this->headers;
        if ($useServiceRole) {
            $headers[1] = 'apikey: ' . $this->serviceRoleKey;
            $headers[2] = 'Authorization: Bearer ' . $this->serviceRoleKey;
        }
        
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
        
        if ($data) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        }
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        curl_close($ch);
        
        if ($error) {
            logMessage("CURL Error: $error", 'ERROR');
            throw new Exception("CURL Error: $error");
        }
        
        $result = json_decode($response, true);
        
        if ($httpCode >= 400) {
            logMessage("Supabase API Error: HTTP $httpCode - " . json_encode($result), 'ERROR');
            throw new Exception("Supabase API Error: " . ($result['error'] ?? 'Unknown error'));
        }
        
        return $result;
    }
    
    /**
     * Аутентификация пользователя
     */
    public function auth($email, $password) {
        $data = [
            'email' => $email,
            'password' => $password
        ];
        
        return $this->makeRequest('/auth/v1/token?grant_type=password', 'POST', $data);
    }
    
    /**
     * Регистрация пользователя
     */
    public function signUp($email, $password, $userData = []) {
        $data = [
            'email' => $email,
            'password' => $password,
            'user_metadata' => $userData
        ];
        
        return $this->makeRequest('/auth/v1/signup', 'POST', $data);
    }
    
    /**
     * Выход пользователя
     */
    public function signOut($accessToken) {
        $headers = $this->headers;
        $headers[] = 'Authorization: Bearer ' . $accessToken;
        
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->url . '/auth/v1/logout');
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        return json_decode($response, true);
    }
    
    /**
     * Получение профиля пользователя
     */
    public function getUser($accessToken) {
        $headers = $this->headers;
        $headers[] = 'Authorization: Bearer ' . $accessToken;
        
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->url . '/auth/v1/user');
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        return json_decode($response, true);
    }
    
    /**
     * Обновление профиля пользователя
     */
    public function updateUser($accessToken, $userData) {
        $headers = $this->headers;
        $headers[] = 'Authorization: Bearer ' . $accessToken;
        
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->url . '/auth/v1/user');
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'PUT');
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($userData));
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        return json_decode($response, true);
    }
    
    /**
     * Вставка данных в таблицу
     */
    public function insert($table, $data, $useServiceRole = false) {
        return $this->makeRequest("/rest/v1/$table", 'POST', $data, $useServiceRole);
    }
    
    /**
     * Выборка данных из таблицы
     */
    public function select($table, $filters = [], $useServiceRole = false) {
        $query = http_build_query($filters);
        $endpoint = "/rest/v1/$table";
        if ($query) {
            $endpoint .= "?$query";
        }
        
        return $this->makeRequest($endpoint, 'GET', null, $useServiceRole);
    }
    
    /**
     * Обновление данных в таблице
     */
    public function update($table, $data, $filters = [], $useServiceRole = false) {
        $query = http_build_query($filters);
        $endpoint = "/rest/v1/$table";
        if ($query) {
            $endpoint .= "?$query";
        }
        
        return $this->makeRequest($endpoint, 'PATCH', $data, $useServiceRole);
    }
    
    /**
     * Удаление данных из таблицы
     */
    public function delete($table, $filters = [], $useServiceRole = false) {
        $query = http_build_query($filters);
        $endpoint = "/rest/v1/$table";
        if ($query) {
            $endpoint .= "?$query";
        }
        
        return $this->makeRequest($endpoint, 'DELETE', null, $useServiceRole);
    }
    
    /**
     * Загрузка файла в Storage
     */
    public function uploadFile($bucket, $path, $fileContent, $contentType = 'application/octet-stream') {
        $headers = [
            'Content-Type: ' . $contentType,
            'apikey: ' . $this->serviceRoleKey,
            'Authorization: Bearer ' . $this->serviceRoleKey
        ];
        
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->url . "/storage/v1/object/$bucket/$path");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
        curl_setopt($ch, CURLOPT_POSTFIELDS, $fileContent);
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        return json_decode($response, true);
    }
    
    /**
     * Получение URL файла
     */
    public function getFileUrl($bucket, $path) {
        return $this->url . "/storage/v1/object/public/$bucket/$path";
    }
    
    /**
     * Удаление файла из Storage
     */
    public function deleteFile($bucket, $path) {
        $headers = [
            'apikey: ' . $this->serviceRoleKey,
            'Authorization: Bearer ' . $this->serviceRoleKey
        ];
        
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->url . "/storage/v1/object/$bucket/$path");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'DELETE');
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        return json_decode($response, true);
    }
}
?> 