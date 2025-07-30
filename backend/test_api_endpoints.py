#!/usr/bin/env python3
"""
Тестовый скрипт для проверки API эндпоинтов
"""
import requests
import json
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

BASE_URL = "http://localhost:8000"

def test_health():
    """Тест health check эндпоинта"""
    print("🔍 Тестирование health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Ответ: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_docs():
    """Тест документации"""
    print("\n🔍 Тестирование документации...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"✅ Docs: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Docs failed: {e}")
        return False

def test_analysis_endpoints():
    """Тест эндпоинтов анализа"""
    print("\n🔍 Тестирование эндпоинтов анализа...")
    
    # Тест cv-analysis-status (публичный эндпоинт)
    try:
        response = requests.get(f"{BASE_URL}/api/v1/analysis/cv-analysis-status")
        print(f"✅ cv-analysis-status endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Система доступна: {data.get('new_system_available', False)}")
            print(f"   AI провайдер: {data.get('ai_provider', 'N/A')}")
            print(f"   Статус: {data.get('status', 'N/A')}")
        else:
            print(f"   Ответ: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ cv-analysis-status failed: {e}")
    
    # Тест summary-report (требует аутентификации)
    try:
        response = requests.get(f"{BASE_URL}/api/v1/analysis/summary-report/me")
        print(f"✅ summary-report endpoint: {response.status_code}")
        if response.status_code == 401:
            print("   Ожидаемо: требуется аутентификация")
        elif response.status_code == 200:
            print("   ✅ Получен отчет")
    except Exception as e:
        print(f"❌ summary-report failed: {e}")
    
    # Тест detailed-analysis (требует аутентификации)
    try:
        response = requests.post(f"{BASE_URL}/api/v1/analysis/detailed-analysis")
        print(f"✅ detailed-analysis endpoint: {response.status_code}")
        if response.status_code == 401:
            print("   Ожидаемо: требуется аутентификация")
        elif response.status_code == 422:
            print("   Ожидаемо: требуется тело запроса")
    except Exception as e:
        print(f"❌ detailed-analysis failed: {e}")

def test_files_endpoints():
    """Тест эндпоинтов файлов"""
    print("\n🔍 Тестирование эндпоинтов файлов...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/files/")
        print(f"✅ files list endpoint exists: {response.status_code}")
        if response.status_code == 501:
            print("   Ожидаемо: эндпоинт временно отключен")
    except Exception as e:
        print(f"❌ files list failed: {e}")

def test_auth_endpoints():
    """Тест эндпоинтов аутентификации"""
    print("\n🔍 Тестирование эндпоинтов аутентификации...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/auth/")
        print(f"✅ auth endpoint exists: {response.status_code}")
    except Exception as e:
        print(f"❌ auth failed: {e}")

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестирования API эндпоинтов...")
    print("=" * 50)
    
    # Проверяем, что сервер запущен
    if not test_health():
        print("\n❌ Сервер не запущен! Запустите: uvicorn main:app --reload")
        return
    
    # Тестируем остальные эндпоинты
    test_docs()
    test_analysis_endpoints()
    test_files_endpoints()
    test_auth_endpoints()
    
    print("\n" + "=" * 50)
    print("✅ Тестирование завершено!")
    print("\n📋 Следующие шаги:")
    print("1. Проверьте, что все эндпоинты отвечают")
    print("2. Если есть ошибки 500, проверьте логи сервера")
    print("3. Для тестирования с аутентификацией используйте Swagger UI: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 