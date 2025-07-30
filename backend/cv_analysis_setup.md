# CV Analysis System Setup Guide

## Overview

The new CV analysis system has been integrated into the backend, replacing the legacy OpenRouter-based analysis with a more comprehensive Google AI-powered system.

## Features

### New System Features
- **Detailed CV Analysis**: Structured JSON output with comprehensive candidate information
- **Achiever Scoring**: Multi-factor scoring system based on achievements, skills, and career progression
- **Candidate Comparison**: Matrix comparison of top candidates
- **Structured Data**: Consistent JSON format for all analyses
- **Fallback Support**: Automatic fallback to legacy system if new system fails

### Legacy System Features (Maintained)
- Simple scoring (1-100)
- Basic recommendations
- PDF/DOCX file generation

## Setup Instructions

### 1. Install Dependencies

Update your requirements.txt with the new dependencies:

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Add the following environment variables to your `.env` file:

```bash
# Google Generative AI API Key (Required for new system)
GOOGLE_API_KEY=your_google_api_key_here

# Optional: AI Model Configuration
AI_MODEL=gemini-pro
AI_TEMPERATURE=0.7

# Legacy OpenRouter (fallback)
OPENROUTER_API_KEY=your_openrouter_key_here
AI_MODEL=mistralai/mistral-small-3.2-24b-instruct:free
```

### 3. Get Google AI API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Add it to your `.env` file

## API Endpoints

### New Endpoints

#### `GET /cv-analysis-status`
Check if the new CV analysis system is available.

**Response:**
```json
{
  "new_system_available": true,
  "features": {
    "detailed_analysis": true,
    "candidate_comparison": true,
    "achiever_scoring": true,
    "structured_output": true
  }
}
```

#### `GET /compare-candidates`
Generate comparison matrix for top candidates.

**Requirements:**
- At least 2 analyzed candidates
- Valid JWT token

**Response:**
```json
{
  "comparison_matrix": {
    "skills_comparison": {...},
    "education_comparison": {...},
    "experience_comparison": {...}
  },
  "key_differentiators": [...],
  "hiring_recommendations": [...],
  "summary": {...},
  "metadata": {...}
}
```

### Updated Endpoints

#### `POST /upload`
Now uses the new CV analysis system by default, with automatic fallback to legacy system.

**Enhanced Response:**
```json
{
  "filename": "cv.pdf",
  "url": "https://...",
  "score": 85,
  "ai_file_url": "https://...",
  "analysis_type": "detailed",
  "achiever_score": 21
}
```

## Analysis Types

### Detailed Analysis (Default)
- Comprehensive candidate profile
- Achiever scoring system
- Skills and experience breakdown
- Recommendations and assessments

### Simple Analysis (Legacy)
- Basic 1-100 score
- Simple recommendations
- Compatible with existing frontend

## Achiever Scoring System

The new system uses a comprehensive scoring approach:

1. **Achievements Score**: 1 point per achievement
2. **Skills Score**: 1 point per skill with 3+ years experience
3. **Responsibilities Score**: Growth in responsibilities (new jobs + within jobs)
4. **Experience Bonus**: 1 point per 3 years of relevant experience
5. **Skills Bonus**: 1 point per 5 skills

**Total Score**: Sum of all components

## Data Structure

### Detailed Analysis Output
```json
{
  "experience_summary": {
    "full_name": "John Doe",
    "years_of_experience": "5",
    "key_roles": ["DevOps Engineer", "Cloud Architect"],
    "achievements": "Led migration to AWS...",
    "skills_1_plus_years": "Docker, Kubernetes, AWS...",
    "technologies": "Docker, Kubernetes, AWS, Terraform...",
    "total_years_of_experience": "5",
    "primary_contact_email": "john@example.com",
    "current_location": "New York, NY",
    "professional_summary": "Experienced DevOps engineer...",
    "cloud_platforms": "AWS, Azure",
    "containerization_orchestration": "Docker, Kubernetes",
    "infrastructure_as_code": "Terraform, CloudFormation",
    "cicd_tools_pipelines": "Jenkins, GitLab CI",
    "monitoring_logging": "Prometheus, ELK Stack",
    "scripting_programming": "Python, Bash, Go",
    "databases": "PostgreSQL, MongoDB",
    "version_control": "Git, GitLab",
    "networking": "VPC, Load Balancers",
    "operating_systems": "Linux, Ubuntu",
    "security_tools": "Vault, AWS IAM",
    "agile_collaboration": "Jira, Confluence",
    "other_technologies": "Ansible, Helm",
    "devops_cloud_experience_years": "5",
    "recent_company_1": "Tech Corp",
    "recent_dates_1": "2020-2023",
    "recent_responsibilities_1": "Led cloud migration...",
    "recent_technologies_1": "AWS, Terraform, Kubernetes",
    "recent_job_title_2": "Senior DevOps Engineer",
    "recent_company_2": "Startup Inc",
    "recent_dates_2": "2018-2020",
    "recent_responsibilities_2": "Built CI/CD pipelines...",
    "recent_technologies_2": "Docker, Jenkins, GitLab",
    "certifications": "AWS Solutions Architect",
    "education_degree": "Bachelor's",
    "education_major": "Computer Science",
    "education_university": "MIT",
    "education_year": "2018",
    "languages": "English, Spanish",
    "desired_role": "Senior DevOps Engineer"
  },
  "achievers_rating": {
    "achievements": {
      "score": 5,
      "achievements_list": ["Led cloud migration", "Reduced deployment time by 80%"]
    },
    "skills": {
      "score": 8,
      "skills_list": ["Docker", "Kubernetes", "AWS", "Terraform", "Jenkins", "Git", "Python", "Linux"]
    },
    "responsibilities": {
      "new_jobs_score": 2,
      "new_jobs_list": ["Junior to Senior DevOps Engineer"],
      "within_job_score": 3,
      "within_job_list": ["Team lead", "Architecture decisions", "Mentoring"],
      "total_score": 5
    },
    "experience_bonus": {
      "score": 1,
      "years_counted": 3
    },
    "skills_bonus": {
      "score": 1,
      "skills_counted": 8
    },
    "overall_score": 20
  },
  "requirements_analysis": {
    "requirements_met": 0.85,
    "matched_requirements": [
      {
        "requirement": "AWS experience",
        "match_level": "High",
        "evidence": "5 years of AWS experience mentioned in recent roles"
      }
    ],
    "missing_requirements": [
      {
        "requirement": "Azure experience",
        "importance": "Medium"
      }
    ]
  },
  "overall_assessment": {
    "match_score": 0.85,
    "strengths": ["Strong cloud experience", "Good automation skills"],
    "weaknesses": ["Limited Azure experience"]
  },
  "recommendations": [
    {
      "area": "Cloud Platforms",
      "suggestion": "Consider gaining Azure experience to broaden cloud expertise"
    }
  ]
}
```

## Migration Guide

### For Existing Users
1. The system automatically falls back to legacy analysis if new system fails
2. Existing analyses remain compatible
3. New uploads use the enhanced system by default
4. Comparison features require at least 2 candidates

### For Frontend Integration
1. Check `/cv-analysis-status` to determine available features
2. Use `/compare-candidates` for candidate comparison
3. Enhanced upload response includes additional fields
4. Handle both detailed and simple analysis formats

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **API Key Issues**: Verify Google AI API key is valid
3. **Analysis Failures**: System automatically falls back to legacy
4. **Comparison Errors**: Need at least 2 candidates

### Debug Mode
Enable detailed logging by setting:
```bash
LOG_LEVEL=DEBUG
```

## Performance Notes

- New system may be slightly slower due to comprehensive analysis
- Comparison matrix generation requires multiple AI calls
- Consider caching results for frequently accessed data
- Monitor API usage to avoid rate limits 