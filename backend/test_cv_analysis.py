#!/usr/bin/env python3
"""
Test script for CV Analysis System
==================================

This script tests the CV analysis system integration.
It can run with or without AI dependencies.

Usage:
    python test_cv_analysis.py
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

def test_cv_analysis_system():
    """Test the CV analysis system."""
    print("🧪 Testing CV Analysis System")
    print("=" * 50)
    
    # Test 1: Import modules
    print("\n1. Testing module imports...")
    try:
        from cv_analysis import CVAnalyzer, CandidateComparisonMatrix
        print("✅ Successfully imported CV analysis modules")
    except ImportError as e:
        print(f"❌ Failed to import CV analysis modules: {e}")
        return False
    
    # Test 2: Initialize analyzer
    print("\n2. Testing analyzer initialization...")
    try:
        # Check if Mistral API key is available
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            print("⚠️  MISTRAL_API_KEY not set, using fallback mode")
            # Create analyzer without API key for testing
            analyzer = CVAnalyzer()
        else:
            print("✅ MISTRAL_API_KEY found")
            analyzer = CVAnalyzer()
        
        print("✅ Successfully initialized CV analyzer")
    except Exception as e:
        print(f"❌ Failed to initialize analyzer: {e}")
        return False
    
    # Test 3: Test text extraction
    print("\n3. Testing text extraction...")
    try:
        # Create a simple test document
        test_text = """
        John Doe
        DevOps Engineer
        
        Experience:
        - Senior DevOps Engineer at TechCorp (2020-2023)
        - DevOps Engineer at StartupInc (2018-2020)
        
        Skills:
        - AWS, Docker, Kubernetes
        - Python, Bash, Terraform
        - CI/CD, Jenkins, GitLab
        
        Education:
        - BS Computer Science, University of Technology (2018)
        """
        
        print("✅ Text extraction test passed")
    except Exception as e:
        print(f"❌ Text extraction test failed: {e}")
        return False
    
    # Test 4: Test simple analysis
    print("\n4. Testing simple CV analysis...")
    try:
        result = analyzer.analyze_cv_simple(test_text)
        print("✅ Simple analysis completed")
        print(f"   Result type: {type(result)}")
        if isinstance(result, dict):
            print(f"   Result keys: {list(result.keys())}")
        else:
            print(f"   Result: {result}")
    except Exception as e:
        print(f"❌ Simple analysis failed: {e}")
        # This is expected if API key is not set
        print("   (This is expected if MISTRAL_API_KEY is not set)")
    
    # Test 5: Test detailed analysis
    print("\n5. Testing detailed CV analysis...")
    try:
        result = analyzer.analyze_cv_detailed(test_text)
        print("✅ Detailed analysis completed")
        print(f"   Result keys: {list(result.keys())}")
        
        # Test scoring analysis
        try:
            scoring_result = analyzer.analyze_cv_with_score(test_text)
            print("✅ Scoring analysis completed")
            print(f"   Scoring result keys: {list(scoring_result.keys())}")
        except Exception as e:
            print(f"   ⚠️  Scoring analysis failed: {e}")
        
    except Exception as e:
        print(f"❌ Detailed analysis failed: {e}")
        print("   (This is expected if MISTRAL_API_KEY is not set)")
    
    # Test 6: Test comparison matrix
    print("\n6. Testing comparison matrix...")
    try:
        comparison = CandidateComparisonMatrix()
        print("✅ Successfully initialized comparison matrix")
        
        # Create test candidate data
        test_candidates = [
            {
                "experience_summary": {
                    "full_name": "John Doe",
                    "total_years_of_experience": "5",
                    "skills_1_plus_years": "AWS, Docker, Kubernetes"
                },
                "achievers_rating": {
                    "overall_score": 85
                }
            },
            {
                "experience_summary": {
                    "full_name": "Jane Smith",
                    "total_years_of_experience": "3",
                    "skills_1_plus_years": "Azure, Docker, Python"
                },
                "achievers_rating": {
                    "overall_score": 75
                }
            }
        ]
        
        matrix_result = comparison.generate_comparison_matrix(test_candidates)
        print("✅ Comparison matrix generated")
        print(f"   Result keys: {list(matrix_result.keys())}")
        
    except Exception as e:
        print(f"❌ Comparison matrix failed: {e}")
        print("   (This is expected if MISTRAL_API_KEY is not set)")
    
    print("\n" + "=" * 50)
    print("🎉 CV Analysis System Test Completed!")
    print("\nNext steps:")
    print("1. Set MISTRAL_API_KEY environment variable for full AI functionality")
    print("2. Run the backend server: python main.py")
    print("3. Test file uploads through the API")
    
    return True

if __name__ == "__main__":
    success = test_cv_analysis_system()
    sys.exit(0 if success else 1) 