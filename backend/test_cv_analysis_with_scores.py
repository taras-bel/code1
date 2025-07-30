#!/usr/bin/env python3
"""
Тестовый скрипт для проверки анализа CV с оценками от 0 до 100
"""
import os
import sys
import json
from pathlib import Path

# Добавляем путь к модулям
sys.path.append(str(Path(__file__).parent))

from cv_analysis.cv_analyzer import CVAnalyzer

def test_cv_analysis_with_scores():
    """Тестирует анализ CV с оценками"""
    print("🧪 Тестирование анализа CV с оценками от 0 до 100")
    print("=" * 60)
    
    # Инициализируем анализатор
    analyzer = CVAnalyzer()
    
    # Тестовый текст CV
    test_cv_text = """
    АЛЕКСАНДР ПЕТРОВ
    Senior Backend Developer
    
    ОПЫТ РАБОТЫ:
    Senior Backend Developer, TechCorp, 2020-2024
    - Разработка микросервисов на Python/FastAPI
    - Интеграция с внешними API
    - Оптимизация производительности баз данных
    - Менторинг junior разработчиков
    
    Backend Developer, StartupXYZ, 2018-2020
    - Разработка REST API на Django
    - Работа с PostgreSQL и Redis
    - Интеграция платежных систем
    
    ОБРАЗОВАНИЕ:
    МГУ им. Ломоносова, Факультет вычислительной математики и кибернетики
    Специализация: Программная инженерия, 2018
    
    НАВЫКИ:
    Технические: Python, FastAPI, Django, PostgreSQL, Redis, Docker, AWS
    Языки: Русский (родной), Английский (B2)
    Инструменты: Git, Linux, VS Code, Postman
    
    ПРОЕКТЫ:
    - E-commerce платформа с микросервисной архитектурой
    - API для мобильного приложения (1M+ пользователей)
    - Система аналитики в реальном времени
    """
    
    # Тестовое описание вакансии
    job_description = """
    Senior Backend Developer
    
    Требования:
    - 5+ лет опыта разработки на Python
    - Опыт работы с FastAPI/Django
    - Знание PostgreSQL, Redis
    - Опыт с микросервисной архитектурой
    - Знание Docker и облачных платформ
    - Английский язык B2+
    
    Обязанности:
    - Разработка и поддержка backend API
    - Оптимизация производительности
    - Код-ревью и менторинг
    - Работа в команде
    """
    
    try:
        print("📋 Анализ CV без описания вакансии...")
        result1 = analyzer.analyze_cv_with_score(test_cv_text)
        
        print("📋 Анализ CV с описанием вакансии...")
        result2 = analyzer.analyze_cv_with_score(test_cv_text, job_description)
        
        print("\n✅ Результаты анализа:")
        print("-" * 40)
        
        print("1. Анализ без вакансии:")
        print(f"   Общая оценка: {result1.get('overall_score', 'N/A')}/100")
        print(f"   Оценка навыков: {result1.get('skills_score', 'N/A')}/100")
        print(f"   Оценка опыта: {result1.get('experience_score', 'N/A')}/100")
        print(f"   Оценка образования: {result1.get('education_score', 'N/A')}/100")
        
        print("\n2. Анализ с вакансией:")
        print(f"   Общая оценка: {result2.get('overall_score', 'N/A')}/100")
        print(f"   Оценка навыков: {result2.get('skills_score', 'N/A')}/100")
        print(f"   Оценка опыта: {result2.get('experience_score', 'N/A')}/100")
        print(f"   Оценка образования: {result2.get('education_score', 'N/A')}/100")
        print(f"   Оценка соответствия: {result2.get('match_score', 'N/A')}/100")
        
        # Проверяем score_breakdown
        if 'score_breakdown' in result2:
            print("\n   Детальная оценка:")
            for key, value in result2['score_breakdown'].items():
                print(f"     {key}: {value}/100")
        
        print("\n📊 Рекомендация:")
        print(f"   {result2.get('recommendation', 'Нет рекомендации')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при анализе: {e}")
        return False

def test_candidate_comparison():
    """Тестирует сравнение кандидатов"""
    print("\n🧪 Тестирование сравнения кандидатов")
    print("=" * 60)
    
    analyzer = CVAnalyzer()
    
    # Тестовые данные кандидатов
    candidates = [
        {
            "name": "Александр Петров",
            "summary": "Senior Backend Developer с 6 годами опыта",
            "skills": {
                "technical": ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker"],
                "soft": ["Лидерство", "Коммуникация", "Менторинг"]
            },
            "experience_years": 6,
            "education": "МГУ, Программная инженерия"
        },
        {
            "name": "Мария Сидорова",
            "summary": "Middle Backend Developer с 3 годами опыта",
            "skills": {
                "technical": ["Python", "Django", "PostgreSQL", "Git"],
                "soft": ["Коммуникация", "Командная работа"]
            },
            "experience_years": 3,
            "education": "МФТИ, Прикладная математика"
        },
        {
            "name": "Дмитрий Козлов",
            "summary": "Junior Backend Developer с 1 годом опыта",
            "skills": {
                "technical": ["Python", "Flask", "SQLite"],
                "soft": ["Обучаемость", "Ответственность"]
            },
            "experience_years": 1,
            "education": "МГТУ им. Баумана, Информатика"
        }
    ]
    
    job_description = """
    Senior Backend Developer
    
    Требования:
    - 5+ лет опыта разработки на Python
    - Опыт работы с FastAPI/Django
    - Знание PostgreSQL, Redis
    - Опыт с микросервисной архитектурой
    - Знание Docker и облачных платформ
    - Английский язык B2+
    
    Обязанности:
    - Разработка и поддержка backend API
    - Оптимизация производительности
    - Код-ревью и менторинг
    - Работа в команде
    """
    
    try:
        print("📊 Сравнение кандидатов...")
        
        # Используем правильные методы для сравнения
        from cv_analysis import CandidateComparisonMatrix
        comparison_matrix = CandidateComparisonMatrix()
        
        # Анализируем каждого кандидата отдельно
        analyzed_candidates = []
        for candidate in candidates:
            # Создаем CV текст для кандидата
            cv_text = f"""
            {candidate['name']}
            {candidate['summary']}
            
            Навыки: {', '.join(candidate['skills']['technical'])}
            Опыт: {candidate['experience_years']} лет
            Образование: {candidate['education']}
            """
            
            # Анализируем кандидата
            analysis_result = analyzer.analyze_cv_with_score(cv_text, job_description)
            analyzed_candidates.append(analysis_result)
        
        # Генерируем матрицу сравнения
        result = comparison_matrix.generate_comparison_matrix(analyzed_candidates)
        
        print("✅ Результаты сравнения:")
        print("-" * 40)
        
        if 'candidates' in result:
            for i, candidate in enumerate(result['candidates']):
                print(f"\n👤 Кандидат {i+1}:")
                print(f"   Общая оценка: {candidate.get('overall_score', 'N/A')}/100")
                print(f"   Оценка навыков: {candidate.get('skills_score', 'N/A')}/100")
                print(f"   Оценка опыта: {candidate.get('experience_score', 'N/A')}/100")
        
        if 'comparison_summary' in result:
            print(f"\n📈 Сводка сравнения:")
            print(f"   {result['comparison_summary']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при сравнении: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестов анализа CV с оценками")
    print("=" * 60)
    
    # Проверяем наличие API ключа
    from config import get_mistral_api_key
    api_key = get_mistral_api_key()
    if not api_key:
        print("❌ MISTRAL_API_KEY не найден в переменных окружения")
        return False
    
    print(f"✅ API ключ найден: {api_key[:10]}...")
    
    # Запускаем тесты
    test1_success = test_cv_analysis_with_scores()
    test2_success = test_candidate_comparison()
    
    print("\n" + "=" * 60)
    if test1_success and test2_success:
        print("🎉 Все тесты прошли успешно!")
        return True
    else:
        print("❌ Некоторые тесты не прошли")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 