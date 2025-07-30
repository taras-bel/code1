"""
CV Analysis System - AI Prompts Module
=====================================

Purpose:
This module contains all the AI prompts used throughout the CV analysis system. These prompts
are designed to guide the AI in analyzing CVs, generating structured data, and creating
comprehensive comparisons between candidates.

How it works:
1. Each prompt is a template string that gets formatted with specific data
2. Prompts are structured to generate consistent JSON responses
3. Different prompts serve different purposes in the analysis pipeline
4. All prompts are optimized for Mistral AI models
5. Responses are designed to be parseable and structured

Dependencies:
- Used by cv_analyzer.py for CV analysis
- Used by comparison_matrix.py for candidate comparison
- Used by export_for_frontend.py for data export
"""

# =============================================================================
# SECTION 1: CV ANALYSIS PROMPT
# =============================================================================
# Primary prompt for analyzing individual CV files against job requirements
# Generates structured JSON with experience summary and achiever ratings

ANALYZE_CV_PROMPT = """
Here is the text extracted from the CV:

{cv_text}

Please analyze the CV and provide a response in the following JSON format:

{{
    "experience_summary": {{
        "summary": "Brief summary of relevant experience",
        "years_of_experience": "Total years of relevant experience",
        "key_roles": ["List of key roles held"],
        "full_name": "Full Name",
        "payment_expectations": "Payment Expectations",
        "achievements": "Achievements",
        "skills_1_plus_years": "Skills (1+ years)",
        "job_titles": "Job Titles",
        "technologies": "Technologies",
        "experience_years": "Experience (years)",
        "responsibilities": "Responsibilities",
        "total_years_of_experience": "Total Years of Experience",
        "primary_contact_email": "Primary Contact Email",
        "primary_contact_phone": "Primary Contact Phone",
        "linkedin_profile_url": "LinkedIn Profile URL",
        "current_location": "Current Location",
        "citizenship_work_permit": "Citizenship & Work Permit",
        "relocation_preference": "Relocation Preference",
        "remote_work_preference": "Remote Work Preference",
        "professional_summary": "Professional Summary",
        "cloud_platforms": "Cloud Platforms",
        "containerization_orchestration": "Containerization & Orchestration",
        "infrastructure_as_code": "Infrastructure as Code (IaC)",
        "cicd_tools_pipelines": "CI/CD Tools & Pipelines",
        "monitoring_logging": "Monitoring & Logging",
        "scripting_programming": "Scripting & Programming",
        "databases": "Databases",
        "version_control": "Version Control",
        "networking": "Networking",
        "operating_systems": "Operating Systems",
        "security_tools": "Security Tools",
        "agile_collaboration": "Agile & Collaboration",
        "other_technologies": "Other Technologies",
        "devops_cloud_experience_years": "DevOps/Cloud Experience (years)",
        "recent_company_1": "Recent Company 1",
        "recent_dates_1": "Recent Dates 1",
        "recent_responsibilities_1": "Recent Responsibilities 1",
        "recent_technologies_1": "Recent Technologies 1",
        "recent_job_title_2": "Recent Job Title 2",
        "recent_company_2": "Recent Company 2",
        "recent_dates_2": "Recent Dates 2",
        "recent_responsibilities_2": "Recent Responsibilities 2",
        "recent_technologies_2": "Recent Technologies 2",
        "certifications": "Certifications",
        "education_degree": "Education Degree",
        "education_major": "Education Major",
        "education_university": "Education University",
        "education_year": "Education Year",
        "languages": "Languages",
        "desired_role": "Desired Role"
    }},
    "achievers_rating": {{
        "achievements": {{
            "score": 5,  // Number of achievements (1 point per achievement)
            "achievements_list": ["List of achievements that contributed to the score"]
        }},
        "skills": {{
            "score": 8,  // Number of skills with 3+ years of daily experience (1 point per skill)
            "skills_list": ["List of skills that contributed to the score"]
        }},
        "responsibilities": {{
            "new_jobs_score": 2,  // Number of job changes with increased responsibilities (1 point per growth)
            "new_jobs_list": ["List of job changes with increased responsibilities"],
            "within_job_score": 3,  // Number of responsibility increases within the same job (1 point per growth)
            "within_job_list": ["List of responsibility increases within jobs"],
            "total_score": 5  // Sum of new_jobs_score and within_job_score
        }},
        "experience_bonus": {{
            "score": 4,  // 1 point per 3 years of relevant experience
            "years_counted": 12  // Number of years that contributed to the bonus
        }},
        "skills_bonus": {{
            "score": 1,  // 1 point per 5 skills
            "skills_counted": 8  // Number of skills that contributed to the bonus
        }},
        "overall_score": 21  // Total sum of all scores (achievements + skills + responsibilities.total_score + experience_bonus + skills_bonus)
    }},
    "requirements_analysis": {{
        "requirements_met": 0.75,  // Score from 0.0 to 1.0
        "matched_requirements": [
            {{
                "requirement": "Specific requirement",
                "match_level": "High/Medium/Low",
                "evidence": "Where in the CV this requirement is met"
            }}
        ],
        "missing_requirements": [
            {{
                "requirement": "Missing requirement",
                "importance": "High/Medium/Low"
            }}
        ]
    }},
    "overall_assessment": {{
        "match_score": 0.75,  // Overall match score from 0.0 to 1.0
        "strengths": ["List of key strengths"],
        "weaknesses": ["List of key weaknesses"]
    }},
    "recommendations": [
        {{
            "area": "Area for improvement",
            "suggestion": "Specific recommendation"
        }}
    ]
}}

Please ensure the response is valid JSON and includes all the fields above.
"""

# =============================================================================
# SECTION 2: CV ANALYSIS WITH JOB DESCRIPTION PROMPT
# =============================================================================
# Enhanced prompt for analyzing CV against specific job requirements

ANALYZE_CV_WITH_JOB_DESCRIPTION_PROMPT = """
Here is the text extracted from the CV:

{cv_text}

Here are the job requirements:

{job_description}

Please analyze the CV against the requirements and provide a response in the following JSON format:

{{
    "experience_summary": {{
        "summary": "Brief summary of relevant experience",
        "years_of_experience": "Total years of relevant experience",
        "key_roles": ["List of key roles held"],
        "full_name": "Full Name",
        "payment_expectations": "Payment Expectations",
        "achievements": "Achievements",
        "skills_1_plus_years": "Skills (1+ years)",
        "job_titles": "Job Titles",
        "technologies": "Technologies",
        "experience_years": "Experience (years)",
        "responsibilities": "Responsibilities",
        "total_years_of_experience": "Total Years of Experience",
        "primary_contact_email": "Primary Contact Email",
        "primary_contact_phone": "Primary Contact Phone",
        "linkedin_profile_url": "LinkedIn Profile URL",
        "current_location": "Current Location",
        "citizenship_work_permit": "Citizenship & Work Permit",
        "relocation_preference": "Relocation Preference",
        "remote_work_preference": "Remote Work Preference",
        "professional_summary": "Professional Summary",
        "cloud_platforms": "Cloud Platforms",
        "containerization_orchestration": "Containerization & Orchestration",
        "infrastructure_as_code": "Infrastructure as Code (IaC)",
        "cicd_tools_pipelines": "CI/CD Tools & Pipelines",
        "monitoring_logging": "Monitoring & Logging",
        "scripting_programming": "Scripting & Programming",
        "databases": "Databases",
        "version_control": "Version Control",
        "networking": "Networking",
        "operating_systems": "Operating Systems",
        "security_tools": "Security Tools",
        "agile_collaboration": "Agile & Collaboration",
        "other_technologies": "Other Technologies",
        "devops_cloud_experience_years": "DevOps/Cloud Experience (years)",
        "recent_company_1": "Recent Company 1",
        "recent_dates_1": "Recent Dates 1",
        "recent_responsibilities_1": "Recent Responsibilities 1",
        "recent_technologies_1": "Recent Technologies 1",
        "recent_job_title_2": "Recent Job Title 2",
        "recent_company_2": "Recent Company 2",
        "recent_dates_2": "Recent Dates 2",
        "recent_responsibilities_2": "Recent Responsibilities 2",
        "recent_technologies_2": "Recent Technologies 2",
        "certifications": "Certifications",
        "education_degree": "Education Degree",
        "education_major": "Education Major",
        "education_university": "Education University",
        "education_year": "Education Year",
        "languages": "Languages",
        "desired_role": "Desired Role"
    }},
    "achievers_rating": {{
        "achievements": {{
            "score": 5,  // Number of achievements (1 point per achievement)
            "achievements_list": ["List of achievements that contributed to the score"]
        }},
        "skills": {{
            "score": 8,  // Number of skills with 3+ years of daily experience (1 point per skill)
            "skills_list": ["List of skills that contributed to the score"]
        }},
        "responsibilities": {{
            "new_jobs_score": 2,  // Number of job changes with increased responsibilities (1 point per growth)
            "new_jobs_list": ["List of job changes with increased responsibilities"],
            "within_job_score": 3,  // Number of responsibility increases within the same job (1 point per growth)
            "within_job_list": ["List of responsibility increases within jobs"],
            "total_score": 5  // Sum of new_jobs_score and within_job_score
        }},
        "experience_bonus": {{
            "score": 4,  // 1 point per 3 years of relevant experience
            "years_counted": 12  // Number of years that contributed to the bonus
        }},
        "skills_bonus": {{
            "score": 1,  // 1 point per 5 skills
            "skills_counted": 8  // Number of skills that contributed to the bonus
        }},
        "overall_score": 21  // Total sum of all scores (achievements + skills + responsibilities.total_score + experience_bonus + skills_bonus)
    }},
    "requirements_analysis": {{
        "requirements_met": 0.75,  // Score from 0.0 to 1.0
        "matched_requirements": [
            {{
                "requirement": "Specific requirement",
                "match_level": "High/Medium/Low",
                "evidence": "Where in the CV this requirement is met"
            }}
        ],
        "missing_requirements": [
            {{
                "requirement": "Missing requirement",
                "importance": "High/Medium/Low"
            }}
        ]
    }},
    "overall_assessment": {{
        "match_score": 0.75,  // Overall match score from 0.0 to 1.0
        "strengths": ["List of key strengths"],
        "weaknesses": ["List of key weaknesses"]
    }},
    "recommendations": [
        {{
            "area": "Area for improvement",
            "suggestion": "Specific recommendation"
        }}
    ]
}}

Please ensure the response is valid JSON and includes all the fields above.
"""

# =============================================================================
# SECTION 3: SIMPLE CV ANALYSIS PROMPT
# =============================================================================
# Simplified prompt for basic CV analysis with scoring

SIMPLE_CV_ANALYSIS_PROMPT = """
Analyze the following CV and provide a comprehensive assessment with scoring:

CV Text:
{cv_text}

Please provide a response in the following JSON format:

{{
    "full_name": "Extracted full name from CV",
    "summary": "Brief professional summary",
    "years_of_experience": "Total years of experience",
    "key_skills": ["List of key technical skills"],
    "technologies": ["List of technologies used"],
    "education": "Education background",
    "certifications": ["List of certifications"],
    "overall_score": <integer 0-100>,
    "skills_score": <integer 0-100>,
    "experience_score": <integer 0-100>,
    "education_score": <integer 0-100>,
    "match_score": <integer 0-100>,
    "strengths": ["List of key strengths"],
    "weaknesses": ["List of areas for improvement"],
    "recommendations": ["List of recommendations"],
    "availability": "Availability",
    "score_breakdown": {{
        "skills_quality": <integer 0-100>,
        "experience_depth": <integer 0-100>,
        "education_quality": <integer 0-100>,
        "overall_impression": <integer 0-100>
    }}
}}

Return ONLY valid JSON. All scores must be integers from 0 to 100. Do NOT copy the example values, analyze the resume and generate unique scores for each candidate. Extract the full name from the resume.
"""

# =============================================================================
# SECTION 4: CANDIDATE COMPARISON MATRIX PROMPT
# =============================================================================
# Prompt for creating detailed comparison matrix of top candidates

CANDIDATE_COMPARISON_MATRIX_PROMPT = """
Please analyze the following candidates and create a detailed comparison matrix highlighting their differences in skills and education.

Candidate Data:
{candidates_data}

Please provide a response in the following JSON format that creates a comprehensive comparison matrix:

{{
    "comparison_summary": {{
        "total_candidates": 3,
        "analysis_date": "YYYY-MM-DD",
        "comparison_focus": "Skills and Education Differences"
    }},
    "candidates": [
        {{
            "name": "Candidate Name",
            "achiever_score": 85,
            "overall_rating": "High/Medium/Low",
            "key_strengths": ["Strength 1", "Strength 2"],
            "unique_advantages": ["Unique skill 1", "Unique skill 2"]
        }}
    ],
    "skills_comparison": {{
        "cloud_platforms": {{
            "candidate_1": {{
                "name": "Candidate 1 Name",
                "skills": ["AWS", "Azure", "GCP"],
                "experience_years": 5,
                "strength_level": "High/Medium/Low"
            }},
            "candidate_2": {{
                "name": "Candidate 2 Name", 
                "skills": ["AWS", "Docker"],
                "experience_years": 3,
                "strength_level": "High/Medium/Low"
            }},
            "candidate_3": {{
                "name": "Candidate 3 Name",
                "skills": ["Azure", "Kubernetes"],
                "experience_years": 4,
                "strength_level": "High/Medium/Low"
            }},
            "differences": {{
                "unique_to_candidate_1": ["GCP"],
                "unique_to_candidate_2": ["Docker"],
                "unique_to_candidate_3": ["Kubernetes"],
                "common_skills": ["AWS"],
                "experience_gap": "2 years between highest and lowest"
            }}
        }},
        "containerization_orchestration": {{
            "candidate_1": {{
                "skills": ["Docker", "Kubernetes", "Helm"],
                "experience_years": 4,
                "strength_level": "High/Medium/Low"
            }},
            "candidate_2": {{
                "skills": ["Docker"],
                "experience_years": 2,
                "strength_level": "High/Medium/Low"
            }},
            "candidate_3": {{
                "skills": ["Kubernetes", "Docker Swarm"],
                "experience_years": 3,
                "strength_level": "High/Medium/Low"
            }},
            "differences": {{
                "unique_to_candidate_1": ["Helm"],
                "unique_to_candidate_2": [],
                "unique_to_candidate_3": ["Docker Swarm"],
                "common_skills": ["Docker"],
                "experience_gap": "2 years between highest and lowest"
            }}
        }},
        "infrastructure_as_code": {{
            "candidate_1": {{
                "skills": ["Terraform", "Ansible", "CloudFormation"],
                "experience_years": 3,
                "strength_level": "High/Medium/Low"
            }},
            "candidate_2": {{
                "skills": ["Terraform"],
                "experience_years": 1,
                "strength_level": "High/Medium/Low"
            }},
            "candidate_3": {{
                "skills": ["Ansible", "Puppet"],
                "experience_years": 2,
                "strength_level": "High/Medium/Low"
            }},
            "differences": {{
                "unique_to_candidate_1": ["CloudFormation"],
                "unique_to_candidate_2": [],
                "unique_to_candidate_3": ["Puppet"],
                "common_skills": [],
                "experience_gap": "2 years between highest and lowest"
            }}
        }},
        "cicd_tools": {{
            "candidate_1": {{
                "skills": ["Jenkins", "GitLab CI", "GitHub Actions"],
                "experience_years": 4,
                "strength_level": "High/Medium/Low"
            }},
            "candidate_2": {{
                "skills": ["Jenkins"],
                "experience_years": 2,
                "strength_level": "High/Medium/Low"
            }},
            "candidate_3": {{
                "skills": ["GitLab CI", "Azure DevOps"],
                "experience_years": 3,
                "strength_level": "High/Medium/Low"
            }},
            "differences": {{
                "unique_to_candidate_1": ["GitHub Actions"],
                "unique_to_candidate_2": [],
                "unique_to_candidate_3": ["Azure DevOps"],
                "common_skills": ["Jenkins"],
                "experience_gap": "2 years between highest and lowest"
            }}
        }},
        "monitoring_logging": {{
            "candidate_1": {{
                "skills": ["Prometheus", "Grafana", "ELK Stack"],
                "experience_years": 3,
                "strength_level": "High/Medium/Low"
            }},
            "candidate_2": {{
                "skills": ["Grafana"],
                "experience_years": 1,
                "strength_level": "High/Medium/Low"
            }},
            "candidate_3": {{
                "skills": ["Prometheus", "Datadog"],
                "experience_years": 2,
                "strength_level": "High/Medium/Low"
            }},
            "differences": {{
                "unique_to_candidate_1": ["ELK Stack"],
                "unique_to_candidate_2": [],
                "unique_to_candidate_3": ["Datadog"],
                "common_skills": ["Prometheus"],
                "experience_gap": "2 years between highest and lowest"
            }}
        }},
        "scripting_programming": {{
            "candidate_1": {{
                "skills": ["Python", "Bash", "Go"],
                "experience_years": 5,
                "strength_level": "High/Medium/Low"
            }},
            "candidate_2": {{
                "skills": ["Python", "Bash"],
                "experience_years": 3,
                "strength_level": "High/Medium/Low"
            }},
            "candidate_3": {{
                "skills": ["Python", "JavaScript"],
                "experience_years": 4,
                "strength_level": "High/Medium/Low"
            }},
            "differences": {{
                "unique_to_candidate_1": ["Go"],
                "unique_to_candidate_2": [],
                "unique_to_candidate_3": ["JavaScript"],
                "common_skills": ["Python"],
                "experience_gap": "2 years between highest and lowest"
            }}
        }}
    }},
    "education_comparison": {{
        "degrees": {{
            "candidate_1": {{
                "degree": "Bachelor's in Computer Science",
                "university": "University Name",
                "graduation_year": 2018,
                "relevance_score": 95
            }},
            "candidate_2": {{
                "degree": "Master's in Information Technology",
                "university": "University Name", 
                "graduation_year": 2020,
                "relevance_score": 90
            }},
            "candidate_3": {{
                "degree": "Bachelor's in Engineering",
                "university": "University Name",
                "graduation_year": 2019,
                "relevance_score": 85
            }},
            "differences": {{
                "highest_degree": "Master's (Candidate 2)",
                "most_recent_graduation": "2020 (Candidate 2)",
                "most_relevant_degree": "Computer Science (Candidate 1)",
                "education_gap": "2 years between oldest and newest graduation"
            }}
        }},
        "certifications": {{
            "candidate_1": {{
                "certifications": ["AWS Solutions Architect", "Kubernetes Administrator"],
                "count": 2,
                "relevance_score": 95
            }},
            "candidate_2": {{
                "certifications": ["AWS Developer"],
                "count": 1,
                "relevance_score": 80
            }},
            "candidate_3": {{
                "certifications": ["Azure Administrator", "Docker Certified"],
                "count": 2,
                "relevance_score": 85
            }},
            "differences": {{
                "most_certifications": "Candidates 1 and 3 (2 each)",
                "highest_relevance": "Candidate 1 (95%)",
                "unique_certifications": {{
                    "candidate_1": ["Kubernetes Administrator"],
                    "candidate_2": ["AWS Developer"],
                    "candidate_3": ["Azure Administrator", "Docker Certified"]
                }}
            }}
        }}
    }},
    "overall_differences": {{
        "strengths_by_candidate": {{
            "candidate_1": {{
                "name": "Candidate 1 Name",
                "primary_strengths": ["Most diverse cloud platform experience", "Strongest education relevance"],
                "unique_advantages": ["Go programming", "ELK Stack", "Helm"],
                "overall_score": 92
            }},
            "candidate_2": {{
                "name": "Candidate 2 Name",
                "primary_strengths": ["Highest degree level", "Most recent education"],
                "unique_advantages": ["Master's degree"],
                "overall_score": 85
            }},
            "candidate_3": {{
                "name": "Candidate 3 Name",
                "primary_strengths": ["Balanced skill set", "Good certification diversity"],
                "unique_advantages": ["Docker Swarm", "Puppet", "Azure DevOps"],
                "overall_score": 88
            }}
        }},
        "key_differentiators": [
            "Candidate 1 has the most comprehensive cloud and monitoring experience",
            "Candidate 2 has the highest formal education level",
            "Candidate 3 has the most diverse tooling experience across different platforms"
        ],
        "recommendations": [
            "For cloud-native roles: Consider Candidate 1",
            "For leadership roles: Consider Candidate 2", 
            "For multi-platform environments: Consider Candidate 3"
        ]
    }}
}}

Please ensure:
1. All candidate names are extracted from the provided data
2. Skills are accurately categorized and compared
3. Education details are properly analyzed for relevance
4. Differences are clearly highlighted with specific examples
5. Overall scores are calculated based on skills, experience, and education relevance
6. The JSON structure is valid and comprehensive
7. All comparisons focus on practical differences that would impact hiring decisions

The output should provide a clear matrix showing what makes each candidate unique and how they compare across key technical and educational dimensions.
"""

# =============================================================================
# SECTION 5: CANDIDATES ANALYSIS PROMPT
# =============================================================================
# Prompt for comprehensive analysis of all candidates together

COMBINE_AND_ANALYZE_CANDIDATES_PROMPT = """
Here is the text extracted from the CVs:

{candidates_data}

Create a list of the Achievers (TOP 5). And let's make scores for a number of columns:
Relevance to Requirement in % - calculate a %, how much DevOps corresponds to the requirements
Achievements - give each achievement 1 point, and sum all these points and put to this field (not text, only number)
Skills - give each skill 1 point if it has at least 3 years of everyday using experience, and sum all these points and put to this field (not text, only number)
Responsibilities - if you see that responsibilities grew than give 1 point, and sum all these points and put to this field (not text, only number)
Job Titles - keep only unique and relevant titles from previous jobs
Technologies - keep only unique and relevant technologies from previous jobs
Experience - in years for all Job titles
Overall Score - Sum all points per row (give and sum 1 point for each 3 years in the relevant field, for each 5 Skills)

Output structure (CSV):
Full Name,
Relevance to Requirement in %,
Payment Expectations,
Achievements,
Skills,
Responsibilities,
Job Titles,
Technologies,
Experience,
Overall Score
"""

# =============================================================================
# SECTION 6: CANDIDATE HIRING PROMPT
# =============================================================================
# Prompt for identifying unique qualities and hiring recommendations

WHICH_CANDIDATE_TO_HIRE_PROMPT = """
Analyze the following candidates and create a spreadsheet of unique qualities for each person:

{candidates_data}

Please provide a response in the following JSON format:

{{
    "candidates": [
        {{
            "name": "Candidate Name",
            "unique_qualities": [
                "Unique quality 1",
                "Unique quality 2",
                "Unique quality 3"
            ],
            "hiring_recommendation": "Strongly Recommend/Recommend/Consider/Not Recommended",
            "best_role_fit": "Specific role this candidate would excel in",
            "key_differentiators": [
                "What makes this candidate stand out"
            ]
        }}
    ],
    "comparison_summary": {{
        "top_candidate": "Name of the best overall candidate",
        "reasoning": "Why this candidate is the top choice",
        "team_fit_analysis": "How candidates would work together",
        "risk_assessment": "Potential risks with each candidate"
    }}
}}

Please ensure:
1. Each candidate's unique qualities are clearly identified
2. Hiring recommendations are based on objective criteria
3. Role fit suggestions are specific and actionable
4. Key differentiators highlight what makes each candidate special
5. The comparison summary provides clear guidance for hiring decisions
""" 