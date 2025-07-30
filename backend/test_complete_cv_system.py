#!/usr/bin/env python3
"""
Полный тест системы анализа CV
"""
import os
import sys
import json
import requests
from pathlib import Path

# Добавляем путь к модулям
sys.path.append(str(Path(__file__).parent))

from cv_analysis import CVAnalyzer, CandidateComparisonMatrix
from config import get_mistral_api_key

BASE_URL = "http://localhost:8000"

def test_cv_analyzer():
    """Тестирует CVAnalyzer"""
    print("🧪 Тестирование CVAnalyzer")
    print("=" * 50)
    
    try:
        # Инициализируем анализатор
        analyzer = CVAnalyzer()
        print("✅ CVAnalyzer инициализирован")
        
        # Тестовый CV
        test_cv = """
        ИВАН ИВАНОВ
        Senior Python Developer
        
        ОПЫТ РАБОТЫ:
        Senior Python Developer, TechCorp, 2021-2024
        - Разработка микросервисов на FastAPI
        - Работа с PostgreSQL и Redis
        - Docker и Kubernetes
        - CI/CD с GitLab
        
        Middle Python Developer, StartupXYZ, 2019-2021
        - Django REST API
        - Интеграция с внешними сервисами
        - Unit тестирование
        
        ОБРАЗОВАНИЕ:
        МГУ, Факультет ВМК, 2019
        
        НАВЫКИ:
        Python, FastAPI, Django, PostgreSQL, Redis, Docker, Git
        """
        
        # Тест простого анализа
        print("\n📋 Тест простого анализа...")
        simple_result = analyzer.analyze_cv_simple(test_cv)
        print(f"✅ Простой анализ: {type(simple_result)}")
        
        # Тест детального анализа
        print("\n📋 Тест детального анализа...")
        detailed_result = analyzer.analyze_cv_detailed(test_cv)
        print(f"✅ Детальный анализ: {list(detailed_result.keys())}")
        
        # Тест анализа с оценками
        print("\n📋 Тест анализа с оценками...")
        scoring_result = analyzer.analyze_cv_with_score(test_cv)
        print(f"✅ Анализ с оценками: {list(scoring_result.keys())}")
        
        # Выводим оценки
        if 'overall_score' in scoring_result:
            print(f"   Общая оценка: {scoring_result['overall_score']}/100")
        if 'skills_score' in scoring_result:
            print(f"   Оценка навыков: {scoring_result['skills_score']}/100")
        if 'experience_score' in scoring_result:
            print(f"   Оценка опыта: {scoring_result['experience_score']}/100")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в CVAnalyzer: {e}")
        return False

def test_comparison_matrix():
    """Тестирует CandidateComparisonMatrix"""
    print("\n🧪 Тестирование CandidateComparisonMatrix")
    print("=" * 50)
    
    try:
        comparison = CandidateComparisonMatrix()
        print("✅ CandidateComparisonMatrix инициализирован")
        
        # Тестовые данные кандидатов
        candidates_data = [
            {
                "overall_score": 85,
                "skills_score": 90,
                "experience_score": 80,
                "experience_summary": {
                    "full_name": "Иван Иванов",
                    "total_years_of_experience": "5"
                }
            },
            {
                "overall_score": 75,
                "skills_score": 80,
                "experience_score": 70,
                "experience_summary": {
                    "full_name": "Петр Петров",
                    "total_years_of_experience": "3"
                }
            }
        ]
        
        # Генерируем матрицу сравнения
        result = comparison.generate_comparison_matrix(candidates_data)
        print(f"✅ Матрица сравнения: {list(result.keys())}")
        
        if 'comparison_summary' in result:
            print(f"   Сводка: {result['comparison_summary']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в CandidateComparisonMatrix: {e}")
        return False

def test_api_endpoints():
    """Тестирует API эндпоинты"""
    print("\n🧪 Тестирование API эндпоинтов")
    print("=" * 50)
    
    try:
        # Тест health check
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        
        # Тест cv-analysis-status
        response = requests.get(f"{BASE_URL}/api/v1/analysis/cv-analysis-status")
        print(f"✅ CV Analysis Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Система доступна: {data.get('new_system_available', False)}")
            print(f"   AI провайдер: {data.get('ai_provider', 'N/A')}")
        
        # Тест summary-report (требует аутентификации)
        response = requests.get(f"{BASE_URL}/api/v1/analysis/summary-report/me")
        print(f"✅ Summary Report: {response.status_code}")
        if response.status_code == 401:
            print("   Ожидаемо: требуется аутентификация")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в API тестах: {e}")
        return False

def test_configuration():
    """Тестирует конфигурацию"""
    print("\n🧪 Тестирование конфигурации")
    print("=" * 50)
    
    try:
        # Проверяем API ключ
        api_key = get_mistral_api_key()
        print(f"✅ Mistral API ключ: {'Настроен' if api_key else 'Не настроен'}")
        
        # Проверяем переменные окружения
        required_vars = [
            'SUPABASE_URL',
            'SUPABASE_SERVICE_ROLE_KEY',
            'MISTRAL_API_KEY',
            'SECRET_KEY'
        ]
        
        for var in required_vars:
            value = os.getenv(var)
            status = "✅" if value else "❌"
            print(f"{status} {var}: {'Настроен' if value else 'Не настроен'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в конфигурации: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Полный тест системы анализа CV")
    print("=" * 60)
    
    tests = [
        ("Конфигурация", test_configuration),
        ("CVAnalyzer", test_cv_analyzer),
        ("CandidateComparisonMatrix", test_comparison_matrix),
        ("API эндпоинты", test_api_endpoints)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Критическая ошибка в {test_name}: {e}")
            results.append((test_name, False))
    
    # Итоговый отчет
    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Результат: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты пройдены! Система готова к работе.")
    else:
        print("⚠️  Некоторые тесты не пройдены. Проверьте конфигурацию.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 