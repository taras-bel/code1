"""
Enhanced CV Analysis Test Script
================================

This script tests the enhanced CV analysis system with detailed achievers_rating structure,
candidate comparison, and new API endpoints.

Features tested:
- Detailed CV analysis with achievers_rating
- Candidate comparison matrix
- Multiple candidates analysis
- Hiring recommendations
- Summary reports
- Candidate insights
- CSV export functionality
"""

import os
import json
import logging
from dotenv import load_dotenv
from cv_analysis import CVAnalyzer, CandidateComparisonMatrix

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_detailed_cv_analysis():
    """Test detailed CV analysis with achievers_rating structure"""
    logger.info("=" * 60)
    logger.info("TESTING DETAILED CV ANALYSIS")
    logger.info("=" * 60)
    
    analyzer = CVAnalyzer()
    
    # Sample CV text
    cv_text = """
    JOHN DOE
    Senior DevOps Engineer
    
    SUMMARY
    Experienced DevOps engineer with 8+ years of experience in cloud infrastructure, 
    CI/CD pipelines, and automation. Proven track record of improving system reliability 
    and reducing deployment times by 70%.
    
    EXPERIENCE
    Senior DevOps Engineer | TechCorp | 2020-2024
    - Led migration of 50+ services to Kubernetes, reducing infrastructure costs by 40%
    - Implemented GitLab CI/CD pipelines reducing deployment time from 2 hours to 15 minutes
    - Managed AWS infrastructure serving 1M+ users with 99.9% uptime
    - Automated monitoring and alerting using Prometheus and Grafana
    
    DevOps Engineer | StartupXYZ | 2018-2020
    - Built Docker containerization strategy for microservices architecture
    - Implemented Terraform for infrastructure as code
    - Reduced server provisioning time from 4 hours to 30 minutes
    
    SKILLS
    - Cloud Platforms: AWS, Azure, GCP
    - Containerization: Docker, Kubernetes, Helm
    - CI/CD: Jenkins, GitLab CI, GitHub Actions
    - Infrastructure as Code: Terraform, Ansible
    - Monitoring: Prometheus, Grafana, ELK Stack
    - Programming: Python, Bash, Go
    
    EDUCATION
    Bachelor of Science in Computer Science | University of Technology | 2018
    
    CERTIFICATIONS
    - AWS Solutions Architect Professional
    - Kubernetes Administrator (CKA)
    - Terraform Associate
    """
    
    # Sample job description
    job_description = """
    Senior DevOps Engineer Position
    
    Requirements:
    - 5+ years of experience in DevOps or related field
    - Strong knowledge of cloud platforms (AWS, Azure, GCP)
    - Experience with containerization (Docker, Kubernetes)
    - Proficiency in CI/CD tools and practices
    - Knowledge of infrastructure as code (Terraform, Ansible)
    - Experience with monitoring and logging tools
    - Programming skills in Python, Bash, or similar
    - Bachelor's degree in Computer Science or related field
    
    Responsibilities:
    - Design and implement cloud infrastructure
    - Build and maintain CI/CD pipelines
    - Automate deployment and configuration management
    - Monitor system performance and reliability
    - Collaborate with development teams
    - Implement security best practices
    """
    
    try:
        # Test detailed analysis
        logger.info("Testing detailed CV analysis...")
        result = analyzer.analyze_cv_detailed(cv_text, job_description)
        
        logger.info("✅ Detailed analysis completed successfully")
        logger.info(f"Result keys: {list(result.keys())}")
        
        # Check for achievers_rating structure
        if "achievers_rating" in result:
            logger.info("✅ Achievers rating structure found")
            achievers = result["achievers_rating"]
            logger.info(f"Achiever score: {achievers.get('overall_score', 'N/A')}")
        else:
            logger.warning("⚠️ Achievers rating structure not found")
        
        # Check for experience_summary structure
        if "experience_summary" in result:
            logger.info("✅ Experience summary structure found")
            experience = result["experience_summary"]
            logger.info(f"Full name: {experience.get('full_name', 'N/A')}")
        else:
            logger.warning("⚠️ Experience summary structure not found")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Detailed analysis failed: {e}")
        return None

def test_candidate_comparison():
    """Test candidate comparison functionality"""
    logger.info("=" * 60)
    logger.info("TESTING CANDIDATE COMPARISON")
    logger.info("=" * 60)
    
    comparison = CandidateComparisonMatrix()
    
    # Sample candidate data
    candidates_data = [
        {
            "full_name": "John Doe",
            "overall_score": 88,
            "skills_score": 90,
            "experience_score": 85,
            "education_score": 80,
            "achievers_rating": {
                "overall_score": 18,
                "achievements": {"score": 5, "achievements_list": ["Led migration to Kubernetes", "Reduced deployment time by 70%"]},
                "skills": {"score": 8, "skills_list": ["AWS", "Kubernetes", "Docker", "Terraform", "Python", "Bash", "Jenkins", "Prometheus"]},
                "responsibilities": {"total_score": 3, "new_jobs_score": 2, "within_job_score": 1},
                "experience_bonus": {"score": 2, "years_counted": 6},
                "skills_bonus": {"score": 1, "skills_counted": 8}
            },
            "experience_summary": {
                "full_name": "John Doe",
                "years_of_experience": "8+ years",
                "cloud_platforms": "AWS, Azure, GCP",
                "containerization_orchestration": "Docker, Kubernetes, Helm",
                "infrastructure_as_code": "Terraform, Ansible",
                "cicd_tools_pipelines": "Jenkins, GitLab CI, GitHub Actions",
                "monitoring_logging": "Prometheus, Grafana, ELK Stack",
                "scripting_programming": "Python, Bash, Go"
            },
            "strengths": ["Strong cloud experience", "Excellent automation skills", "Proven leadership"],
            "weaknesses": ["Limited Azure experience", "Could improve documentation skills"]
        },
        {
            "full_name": "Jane Smith",
            "overall_score": 92,
            "skills_score": 95,
            "experience_score": 90,
            "education_score": 85,
            "achievers_rating": {
                "overall_score": 22,
                "achievements": {"score": 6, "achievements_list": ["Built scalable microservices", "Improved system reliability by 50%", "Led team of 5 engineers"]},
                "skills": {"score": 10, "skills_list": ["AWS", "Kubernetes", "Docker", "Terraform", "Ansible", "Python", "Go", "Bash", "Jenkins", "Prometheus"]},
                "responsibilities": {"total_score": 4, "new_jobs_score": 3, "within_job_score": 1},
                "experience_bonus": {"score": 2, "years_counted": 6},
                "skills_bonus": {"score": 2, "skills_counted": 10}
            },
            "experience_summary": {
                "full_name": "Jane Smith",
                "years_of_experience": "10+ years",
                "cloud_platforms": "AWS, GCP",
                "containerization_orchestration": "Docker, Kubernetes, Docker Swarm",
                "infrastructure_as_code": "Terraform, CloudFormation",
                "cicd_tools_pipelines": "Jenkins, GitLab CI",
                "monitoring_logging": "Prometheus, Grafana, Datadog",
                "scripting_programming": "Python, Go, JavaScript"
            },
            "strengths": ["Extensive experience", "Strong technical leadership", "Excellent problem-solving"],
            "weaknesses": ["Could improve Azure knowledge", "Limited experience with some newer tools"]
        },
        {
            "full_name": "Bob Johnson",
            "overall_score": 75,
            "skills_score": 70,
            "experience_score": 80,
            "education_score": 75,
            "achievers_rating": {
                "overall_score": 15,
                "achievements": {"score": 3, "achievements_list": ["Implemented CI/CD pipeline", "Reduced server costs by 30%"]},
                "skills": {"score": 6, "skills_list": ["AWS", "Docker", "Terraform", "Python", "Bash", "Jenkins"]},
                "responsibilities": {"total_score": 2, "new_jobs_score": 1, "within_job_score": 1},
                "experience_bonus": {"score": 2, "years_counted": 6},
                "skills_bonus": {"score": 1, "skills_counted": 6}
            },
            "experience_summary": {
                "full_name": "Bob Johnson",
                "years_of_experience": "5+ years",
                "cloud_platforms": "AWS",
                "containerization_orchestration": "Docker",
                "infrastructure_as_code": "Terraform",
                "cicd_tools_pipelines": "Jenkins",
                "monitoring_logging": "CloudWatch",
                "scripting_programming": "Python, Bash"
            },
            "strengths": ["Solid AWS experience", "Good automation skills", "Reliable team player"],
            "weaknesses": ["Limited Kubernetes experience", "Could improve monitoring skills", "Less leadership experience"]
        }
    ]
    
    try:
        # Test comparison matrix generation
        logger.info("Testing comparison matrix generation...")
        comparison_result = comparison.generate_comparison_matrix(candidates_data, top_n=3)
        
        logger.info("✅ Comparison matrix generated successfully")
        logger.info(f"Result keys: {list(comparison_result.keys())}")
        
        # Test multiple candidates analysis
        logger.info("Testing multiple candidates analysis...")
        analysis_result = comparison.analyze_candidates_together(candidates_data)
        
        logger.info("✅ Multiple candidates analysis completed")
        logger.info(f"Analysis result keys: {list(analysis_result.keys())}")
        
        # Test hiring recommendations
        logger.info("Testing hiring recommendations...")
        recommendations = comparison.get_hiring_recommendations(candidates_data)
        
        logger.info("✅ Hiring recommendations generated")
        logger.info(f"Recommendations result keys: {list(recommendations.keys())}")
        
        # Test summary report
        logger.info("Testing summary report generation...")
        summary = comparison.create_summary_report(candidates_data)
        
        logger.info("✅ Summary report generated")
        logger.info(f"Summary keys: {list(summary.keys())}")
        
        # Test candidate insights
        logger.info("Testing candidate insights...")
        insights = comparison.get_candidate_insights(candidates_data[0])
        
        logger.info("✅ Candidate insights generated")
        logger.info(f"Insights keys: {list(insights.keys())}")
        
        # Test CSV export
        logger.info("Testing CSV export...")
        csv_data = comparison.export_comparison_to_csv(comparison_result)
        
        logger.info("✅ CSV export completed")
        logger.info(f"CSV data length: {len(csv_data)} characters")
        
        return {
            "comparison_matrix": comparison_result,
            "analysis": analysis_result,
            "recommendations": recommendations,
            "summary": summary,
            "insights": insights,
            "csv_data": csv_data
        }
        
    except Exception as e:
        logger.error(f"❌ Candidate comparison failed: {e}")
        return None

def test_simple_analysis():
    """Test simple CV analysis"""
    logger.info("=" * 60)
    logger.info("TESTING SIMPLE CV ANALYSIS")
    logger.info("=" * 60)
    
    analyzer = CVAnalyzer()
    
    cv_text = """
    ALEX BROWN
    DevOps Engineer
    
    SUMMARY
    DevOps engineer with 3 years of experience in AWS, Docker, and CI/CD.
    
    EXPERIENCE
    DevOps Engineer | CompanyABC | 2021-2024
    - Managed AWS infrastructure
    - Built Docker containers
    - Implemented Jenkins pipelines
    
    SKILLS
    - AWS, Docker, Jenkins, Python, Bash
    
    EDUCATION
    Bachelor of Science in IT | State University | 2021
    """
    
    try:
        logger.info("Testing simple CV analysis...")
        result = analyzer.analyze_cv_simple(cv_text)
        
        logger.info("✅ Simple analysis completed successfully")
        logger.info(f"Result keys: {list(result.keys())}")
        
        # Check for basic scoring
        if "overall_score" in result:
            logger.info(f"Overall score: {result['overall_score']}")
        if "skills_score" in result:
            logger.info(f"Skills score: {result['skills_score']}")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Simple analysis failed: {e}")
        return None

def main():
    """Main test function"""
    logger.info("🚀 Starting Enhanced CV Analysis Tests")
    logger.info("=" * 80)
    
    # Test 1: Detailed CV Analysis
    detailed_result = test_detailed_cv_analysis()
    
    # Test 2: Simple CV Analysis
    simple_result = test_simple_analysis()
    
    # Test 3: Candidate Comparison
    comparison_results = test_candidate_comparison()
    
    # Summary
    logger.info("=" * 80)
    logger.info("📊 TEST SUMMARY")
    logger.info("=" * 80)
    
    if detailed_result:
        logger.info("✅ Detailed CV Analysis: PASSED")
    else:
        logger.error("❌ Detailed CV Analysis: FAILED")
    
    if simple_result:
        logger.info("✅ Simple CV Analysis: PASSED")
    else:
        logger.error("❌ Simple CV Analysis: FAILED")
    
    if comparison_results:
        logger.info("✅ Candidate Comparison: PASSED")
        logger.info("✅ Multiple Candidates Analysis: PASSED")
        logger.info("✅ Hiring Recommendations: PASSED")
        logger.info("✅ Summary Reports: PASSED")
        logger.info("✅ Candidate Insights: PASSED")
        logger.info("✅ CSV Export: PASSED")
    else:
        logger.error("❌ Candidate Comparison: FAILED")
    
    logger.info("=" * 80)
    logger.info("🎉 Enhanced CV Analysis Tests Completed")
    
    # Save results to file
    results = {
        "detailed_analysis": detailed_result,
        "simple_analysis": simple_result,
        "comparison_results": comparison_results,
        "test_timestamp": "2024-01-01T00:00:00Z"
    }
    
    with open("enhanced_cv_analysis_test_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    logger.info("💾 Test results saved to enhanced_cv_analysis_test_results.json")

if __name__ == "__main__":
    main() 