"""
CV Analysis System Module
========================

This module provides comprehensive CV analysis functionality using Google's Generative AI.
It includes text extraction, AI analysis, structured data generation, and candidate comparison.

Main Components:
- CVAnalyzer: Core CV analysis functionality
- CandidateComparisonMatrix: Candidate comparison and ranking
- prompts: AI prompts for analysis and comparison

Usage:
    from cv_analysis import CVAnalyzer, CandidateComparisonMatrix
    
    # Initialize analyzer
    analyzer = CVAnalyzer()
    
    # Analyze CV
    result = analyzer.analyze_cv_detailed(cv_text)
    
    # Compare candidates
    comparison = CandidateComparisonMatrix()
    matrix = comparison.generate_comparison_matrix(candidates_data)
"""

from .cv_analyzer import CVAnalyzer
from .comparison_matrix import CandidateComparisonMatrix

__all__ = ['CVAnalyzer', 'CandidateComparisonMatrix'] 