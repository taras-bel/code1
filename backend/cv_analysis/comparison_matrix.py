"""
Candidate Comparison Matrix Module
=================================

This module provides functionality for comparing multiple candidates and generating
detailed comparison matrices. It uses the CVAnalyzer to perform AI-powered comparisons
and provides structured output for hiring decisions.

Features:
- Top candidate selection based on achiever scores
- Detailed skills comparison matrix
- Education and experience comparison
- Hiring recommendations
- Unique candidate qualities identification
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from .cv_analyzer import CVAnalyzer

logger = logging.getLogger(__name__)

class CandidateComparisonMatrix:
    """
    Класс для создания матрицы сравнения кандидатов
    """
    
    def __init__(self):
        """Инициализация анализатора"""
        self.analyzer = CVAnalyzer()

    def select_top_candidates(self, candidates_data: List[Dict[str, Any]], top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Выбирает топ кандидатов на основе achiever score
        
        Args:
            candidates_data: Список данных кандидатов
            top_n: Количество топ кандидатов для выбора
            
        Returns:
            Список топ кандидатов, отсортированных по achiever score
        """
        try:
            # Извлекаем achiever scores
            scored_candidates = []
            for candidate in candidates_data:
                # Пытаемся получить achiever score из разных возможных мест
                achiever_score = 0
                
                # Проверяем achievers_rating структуру
                if "achievers_rating" in candidate:
                    achievers = candidate["achievers_rating"]
                    if "overall_score" in achievers:
                        achiever_score = achievers["overall_score"]
                
                # Проверяем overall_score в корне
                elif "overall_score" in candidate:
                    achiever_score = candidate["overall_score"]
                
                # Проверяем score_breakdown
                elif "score_breakdown" in candidate:
                    breakdown = candidate["score_breakdown"]
                    if "overall_impression" in breakdown:
                        achiever_score = breakdown["overall_impression"]
                
                scored_candidates.append({
                    "candidate_data": candidate,
                    "achiever_score": achiever_score
                })
            
            # Сортируем по achiever score (по убыванию)
            scored_candidates.sort(key=lambda x: x["achiever_score"], reverse=True)
            
            # Выбираем топ N кандидатов
            top_candidates = scored_candidates[:top_n]
            
            logger.info(f"Selected top {len(top_candidates)} candidates with scores: {[c['achiever_score'] for c in top_candidates]}")
            
            return [c["candidate_data"] for c in top_candidates]
            
        except Exception as e:
            logger.error(f"Error selecting top candidates: {e}")
            # Возвращаем первых N кандидатов в случае ошибки
            return candidates_data[:top_n]
    
    def generate_comparison_matrix(self, candidates_data: List[Dict[str, Any]], top_n: int = 3) -> Dict[str, Any]:
        """
        Генерирует детальную матрицу сравнения кандидатов
        
        Args:
            candidates_data: Список данных кандидатов
            top_n: Количество топ кандидатов для сравнения
            
        Returns:
            Словарь с матрицей сравнения
        """
        try:
            # Выбираем топ кандидатов
            top_candidates = self.select_top_candidates(candidates_data, top_n)
            
            if not top_candidates:
                return {
                    "error": "No candidates available for comparison",
                    "comparison_summary": {
                        "total_candidates": 0,
                        "analysis_date": datetime.now().isoformat(),
                        "comparison_focus": "No candidates to compare"
                    }
                }
            
            # Генерируем матрицу сравнения через AI
            comparison_result = self.analyzer.generate_comparison_matrix(top_candidates)
            
            # Добавляем метаданные
            comparison_result["metadata"] = {
                "generated_at": datetime.now().isoformat(),
                "total_candidates_analyzed": len(candidates_data),
                "top_candidates_selected": len(top_candidates),
                "selection_criteria": "achiever_score"
            }
            
            return comparison_result
            
        except Exception as e:
            logger.error(f"Error generating comparison matrix: {e}")
            return {
                "error": f"Failed to generate comparison matrix: {str(e)}",
                "candidates_data": candidates_data
            }
    
    def analyze_candidates_together(self, candidates_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Анализирует всех кандидатов вместе для получения общего представления
        
        Args:
            candidates_data: Список данных кандидатов
            
        Returns:
            Результат совместного анализа
        """
        try:
            if not candidates_data:
                return {
                    "error": "No candidates data provided",
                    "analysis_summary": "No candidates to analyze"
                }
            
            # Выполняем совместный анализ через AI
            analysis_result = self.analyzer.analyze_multiple_candidates(candidates_data)
            
            # Добавляем метаданные
            analysis_result["metadata"] = {
                "generated_at": datetime.now().isoformat(),
                "total_candidates": len(candidates_data),
                "analysis_type": "comprehensive_group_analysis"
            }
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error analyzing candidates together: {e}")
            return {
                "error": f"Failed to analyze candidates together: {str(e)}",
                "candidates_data": candidates_data
            }
    
    def get_hiring_recommendations(self, candidates_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Получает рекомендации по найму для кандидатов
        
        Args:
            candidates_data: Список данных кандидатов
            
        Returns:
            Рекомендации по найму
        """
        try:
            if not candidates_data:
                return {
                    "error": "No candidates data provided",
                    "recommendations": []
                }
            
            # Получаем рекомендации через AI
            recommendations = self.analyzer.get_hiring_recommendations(candidates_data)
            
            # Добавляем метаданные
            recommendations["metadata"] = {
                "generated_at": datetime.now().isoformat(),
                "total_candidates": len(candidates_data),
                "analysis_type": "hiring_recommendations"
            }
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting hiring recommendations: {e}")
            return {
                "error": f"Failed to get hiring recommendations: {str(e)}",
                "candidates_data": candidates_data
            }
    
    def create_summary_report(self, candidates_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Создает сводный отчет по всем кандидатам
        
        Args:
            candidates_data: Список данных кандидатов
            
        Returns:
            Сводный отчет
        """
        try:
            if not candidates_data:
                return {
                    "error": "No candidates data provided",
                    "summary": "No candidates to summarize"
                }
            
            # Выбираем топ кандидатов
            top_candidates = self.select_top_candidates(candidates_data, 5)
            
            # Создаем сводку
            summary = {
                "total_candidates": len(candidates_data),
                "top_candidates": [],
                "score_distribution": {
                    "excellent": 0,  # 90-100
                    "good": 0,       # 70-89
                    "average": 0,    # 50-69
                    "below_average": 0  # 0-49
                },
                "average_scores": {
                    "overall": 0,
                    "skills": 0,
                    "experience": 0,
                    "education": 0
                },
                "generated_at": datetime.now().isoformat()
            }
            
            # Анализируем распределение оценок
            total_overall = 0
            total_skills = 0
            total_experience = 0
            total_education = 0
            
            for candidate in candidates_data:
                overall_score = candidate.get("overall_score", 0)
                skills_score = candidate.get("skills_score", 0)
                experience_score = candidate.get("experience_score", 0)
                education_score = candidate.get("education_score", 0)
                
                # Распределение по категориям
                if overall_score >= 90:
                    summary["score_distribution"]["excellent"] += 1
                elif overall_score >= 70:
                    summary["score_distribution"]["good"] += 1
                elif overall_score >= 50:
                    summary["score_distribution"]["average"] += 1
                else:
                    summary["score_distribution"]["below_average"] += 1
                
                # Суммируем для средних значений
                total_overall += overall_score
                total_skills += skills_score
                total_experience += experience_score
                total_education += education_score
            
            # Вычисляем средние значения
            if candidates_data:
                summary["average_scores"]["overall"] = total_overall / len(candidates_data)
                summary["average_scores"]["skills"] = total_skills / len(candidates_data)
                summary["average_scores"]["experience"] = total_experience / len(candidates_data)
                summary["average_scores"]["education"] = total_education / len(candidates_data)
            
            # Добавляем информацию о топ кандидатах
            for i, candidate in enumerate(top_candidates, 1):
                candidate_summary = {
                    "rank": i,
                    "name": candidate.get("full_name", f"Candidate {i}"),
                    "overall_score": candidate.get("overall_score", 0),
                    "skills_score": candidate.get("skills_score", 0),
                    "experience_score": candidate.get("experience_score", 0),
                    "education_score": candidate.get("education_score", 0),
                    "key_strengths": candidate.get("strengths", [])[:3],  # Топ 3 сильные стороны
                    "summary": candidate.get("summary", "")[:200]  # Первые 200 символов
                }
                summary["top_candidates"].append(candidate_summary)
            
            return summary
            
        except Exception as e:
            logger.error(f"Error creating summary report: {e}")
            return {
                "error": f"Failed to create summary report: {str(e)}",
                "candidates_data": candidates_data
            }
    
    def export_comparison_to_csv(self, comparison_matrix: Dict[str, Any]) -> str:
        """
        Экспортирует матрицу сравнения в CSV формат
        
        Args:
            comparison_matrix: Матрица сравнения
            
        Returns:
            CSV строка
        """
        try:
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Записываем заголовок
            writer.writerow([
                "Comparison Category",
                "Candidate 1",
                "Candidate 2", 
                "Candidate 3",
                "Notes"
            ])
            
            # Извлекаем данные кандидатов
            candidates = comparison_matrix.get("candidates", [])
            skills_comparison = comparison_matrix.get("skills_comparison", {})
            
            # Записываем имена кандидатов
            candidate_names = [c.get("name", f"Candidate {i+1}") for i, c in enumerate(candidates)]
            writer.writerow(["Candidate Names"] + candidate_names + [""])
            
            # Записываем achiever scores
            achiever_scores = [c.get("achiever_score", 0) for c in candidates]
            writer.writerow(["Achiever Scores"] + achiever_scores + [""])
            
            # Записываем сравнение навыков
            writer.writerow([])
            writer.writerow(["Skills Comparison"])
            
            for skill_category, skill_data in skills_comparison.items():
                if isinstance(skill_data, dict) and "candidate_1" in skill_data:
                    writer.writerow([skill_category])
                    
                    # Навыки кандидатов
                    for i in range(1, 4):
                        candidate_key = f"candidate_{i}"
                        if candidate_key in skill_data:
                            candidate_skills = skill_data[candidate_key]
                            skills_list = candidate_skills.get("skills", [])
                            experience = candidate_skills.get("experience_years", 0)
                            writer.writerow([
                                f"  Candidate {i} Skills",
                                ", ".join(skills_list),
                                f"{experience} years",
                                "",
                                ""
                            ])
                    
                    # Различия
                    differences = skill_data.get("differences", {})
                    unique_skills = []
                    for i in range(1, 4):
                        unique_key = f"unique_to_candidate_{i}"
                        if unique_key in differences:
                            unique_skills.extend(differences[unique_key])
                    
                    if unique_skills:
                        writer.writerow([
                            "  Unique Skills",
                            ", ".join(unique_skills),
                            "",
                            "",
                            ""
                        ])
                    
                    writer.writerow([])
            
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Error exporting comparison to CSV: {e}")
            return f"Error: {str(e)}"
    
    def get_candidate_insights(self, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Получает инсайты по конкретному кандидату
        
        Args:
            candidate_data: Данные кандидата
            
        Returns:
            Инсайты по кандидату
        """
        try:
            insights = {
                "name": candidate_data.get("full_name", "Unknown"),
                "overall_score": candidate_data.get("overall_score", 0),
                "score_breakdown": candidate_data.get("score_breakdown", {}),
                "strengths": candidate_data.get("strengths", []),
                "weaknesses": candidate_data.get("weaknesses", []),
                "recommendations": candidate_data.get("recommendations", []),
                "achievers_rating": candidate_data.get("achievers_rating", {}),
                "experience_summary": candidate_data.get("experience_summary", {}),
                "insights": {
                    "score_category": self._get_score_category(candidate_data.get("overall_score", 0)),
                    "key_achievements": self._extract_achievements(candidate_data),
                    "skill_gaps": self._identify_skill_gaps(candidate_data),
                    "career_progression": self._analyze_career_progression(candidate_data),
                    "recommendation_level": self._get_recommendation_level(candidate_data.get("overall_score", 0))
                }
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Error getting candidate insights: {e}")
            return {
                "error": f"Failed to get candidate insights: {str(e)}",
                "candidate_data": candidate_data
            }
    
    def _get_score_category(self, score: int) -> str:
        """Определяет категорию оценки"""
        if score >= 90:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 50:
            return "Average"
        else:
            return "Below Average"
    
    def _extract_achievements(self, candidate_data: Dict[str, Any]) -> List[str]:
        """Извлекает достижения кандидата"""
        achievements = []
        
        # Из achievers_rating
        achievers = candidate_data.get("achievers_rating", {})
        if "achievements" in achievers:
            achievements_list = achievers["achievements"].get("achievements_list", [])
            achievements.extend(achievements_list)
        
        # Из experience_summary
        experience = candidate_data.get("experience_summary", {})
        if "achievements" in experience:
            achievements.append(experience["achievements"])
        
        return achievements[:5]  # Топ 5 достижений
    
    def _identify_skill_gaps(self, candidate_data: Dict[str, Any]) -> List[str]:
        """Определяет пробелы в навыках"""
        # Это можно расширить на основе требований вакансии
        return ["Skill gap analysis requires job requirements"]
    
    def _analyze_career_progression(self, candidate_data: Dict[str, Any]) -> str:
        """Анализирует карьерный рост"""
        achievers = candidate_data.get("achievers_rating", {})
        responsibilities = achievers.get("responsibilities", {})
        
        new_jobs_score = responsibilities.get("new_jobs_score", 0)
        within_job_score = responsibilities.get("within_job_score", 0)
        
        if new_jobs_score > 0 or within_job_score > 0:
            return "Strong career progression with increasing responsibilities"
        else:
            return "Limited career progression evidence"
    
    def _get_recommendation_level(self, score: int) -> str:
        """Определяет уровень рекомендации"""
        if score >= 90:
            return "Strongly Recommend"
        elif score >= 70:
            return "Recommend"
        elif score >= 50:
            return "Consider"
        else:
            return "Not Recommended" 