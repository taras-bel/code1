import os
import json
import csv
from pathlib import Path
from .cv_analyzer import CVAnalyzer
from .comparison_matrix import CandidateComparisonMatrix

# Директории
AI_RESPONSES_DIR = Path('backend/output/ai_responses')
EXPORT_DIR = Path('backend/output')
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
AI_RESPONSES_DIR.mkdir(parents=True, exist_ok=True)

# 1. Собираем все JSON-ответы по кандидатам
def collect_candidates():
    candidates = []
    for file in AI_RESPONSES_DIR.glob('*.json'):
        with open(file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                candidates.append(data)
            except Exception:
                continue
    return candidates

# 2. Формируем candidates_datatable.json для фронта
def export_datatable_json(candidates):
    data = []
    for c in candidates:
        exp = c.get('experience_summary', {})
        ach = c.get('achievers_rating', {})
        data.append({
            'full_name': exp.get('full_name'),
            'relevance_percent': exp.get('relevance_percent', ''),
            'payment': exp.get('payment_expectations', ''),
            'achievements': ach.get('achievements', {}).get('score', ''),
            'skills': ach.get('skills', {}).get('score', ''),
            'growth': ach.get('responsibilities', {}).get('total_score', ''),
            'experience': exp.get('total_years_of_experience', ''),
            'score': ach.get('overall_score', ''),
            'unique_skills': ach.get('skills', {}).get('skills_list', []),
            'certifications': exp.get('certifications', ''),
            'education': exp.get('education_degree', ''),
            'specialization': exp.get('education_major', ''),
            'unique_experience': exp.get('professional_summary', ''),
            'raw': c
        })
    with open(EXPORT_DIR / 'candidates_datatable.json', 'w', encoding='utf-8') as f:
        json.dump({'data': data}, f, ensure_ascii=False, indent=2)

# 3. Формируем candidates_summary.csv для фронта
def export_summary_csv(candidates):
    headers = [
        'full_name', 'relevance_percent', 'payment', 'achievements', 'skills', 'growth', 'experience', 'score'
    ]
    with open(EXPORT_DIR / 'candidates_summary.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for c in candidates:
            exp = c.get('experience_summary', {})
            ach = c.get('achievers_rating', {})
            writer.writerow([
                exp.get('full_name'),
                exp.get('relevance_percent', ''),
                exp.get('payment_expectations', ''),
                ach.get('achievements', {}).get('score', ''),
                ach.get('skills', {}).get('score', ''),
                ach.get('responsibilities', {}).get('total_score', ''),
                exp.get('total_years_of_experience', ''),
                ach.get('overall_score', '')
            ])

# 4. Генерируем detailed comparison matrix для топ-3 кандидатов
def export_comparison_matrix(candidates):
    matrix = CandidateComparisonMatrix()
    result = matrix.generate_comparison_matrix_ethalon(candidates, top_n=3)
    with open(EXPORT_DIR / 'candidate_comparison_matrix.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    candidates = collect_candidates()
    if not candidates:
        print('No candidates found!')
        exit(0)
    export_datatable_json(candidates)
    export_summary_csv(candidates)
    export_comparison_matrix(candidates)
    print('Export complete!') 