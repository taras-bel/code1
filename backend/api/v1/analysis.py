"""
Analysis endpoints for API v1
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Path
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from datetime import datetime
import uuid

# from database.connection import get_db  # Commented out - not needed with Supabase SDK
from database.models import Analysis, UploadedFile, User, RateLimit, Profile
from security.auth import decode_jwt_token
from tasks.analysis_tasks import analyze_cv_background
from supabase import create_client, Client
import os
from cv_analysis import CVAnalyzer, CandidateComparisonMatrix
import base64
from config import BUCKET_NAME, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY

router = APIRouter()

# Security
bearer_scheme = HTTPBearer()

# Supabase client
if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment variables")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# Pydantic models
class AnalysisCreate(BaseModel):
    job_description: str

class AnalysisResponse(BaseModel):
    id: str
    job_description: str
    status: str
    results: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: datetime

class CandidateComparisonRequest(BaseModel):
    candidate_ids: List[str]
    top_n: Optional[int] = 3

class DetailedAnalysisRequest(BaseModel):
    cv_text: str
    job_description: Optional[str] = ""

class ComparisonMatrixResponse(BaseModel):
    comparison_matrix: Dict[str, Any]
    metadata: Dict[str, Any]

class CandidateInsightsResponse(BaseModel):
    insights: Dict[str, Any]
    metadata: Dict[str, Any]

# Initialize analyzers
cv_analyzer = CVAnalyzer()
comparison_matrix = CandidateComparisonMatrix()

@router.post("/", response_model=AnalysisResponse)
async def create_analysis(
    analysis_data: AnalysisCreate,
    credentials=Depends(bearer_scheme)
):
    """
    Create a new CV analysis (Profile-based auth)
    """
    try:
        profile_id = decode_jwt_token(credentials.credentials)
        
        # Sanitize job_description to remove null bytes
        clean_job_description = analysis_data.job_description.replace('\x00', '')
        
        # Создаем анализ через Supabase
        data = {
            "user_id": profile_id,
            "job_description": clean_job_description,
            "status": "pending"
        }
        
        resp = supabase.table("analyses").insert(data).execute()
        if not resp.data or not resp.data[0].get("id"):
            raise HTTPException(status_code=500, detail="Failed to create analysis")
        
        analysis = resp.data[0]
        updated_at = analysis.get("updated_at")
        if isinstance(updated_at, str):
            try:
                updated_at = datetime.fromisoformat(updated_at)
            except Exception:
                updated_at = datetime.utcnow()
        elif updated_at is None:
            updated_at = datetime.utcnow()
        
        return AnalysisResponse(
            id=analysis["id"],
            job_description=analysis["job_description"],
            status=analysis["status"],
            results=analysis.get("results"),
            created_at=analysis["created_at"],
            updated_at=updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error creating analysis: {str(e)}")

@router.post("/detailed-analysis")
async def analyze_cv_detailed(
    request: DetailedAnalysisRequest,
    credentials=Depends(bearer_scheme)
):
    """
    Perform detailed CV analysis with achievers_rating structure
    """
    try:
        profile_id = decode_jwt_token(credentials.credentials)
        
        # Perform detailed analysis
        result = cv_analyzer.analyze_cv_detailed(
            cv_text=request.cv_text,
            job_description=request.job_description or ""
        )
        
        return {
            "success": True,
            "analysis": result,
            "metadata": {
                "analyzed_at": datetime.utcnow().isoformat(),
                "user_id": profile_id,
                "analysis_type": "detailed"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/compare-candidates", response_model=ComparisonMatrixResponse)
async def compare_candidates(
    request: CandidateComparisonRequest,
    credentials=Depends(bearer_scheme)
):
    """
    Generate comparison matrix for top candidates
    """
    try:
        profile_id = decode_jwt_token(credentials.credentials)
        
        # Get candidate data from database
        candidates_data = []
        for candidate_id in request.candidate_ids:
            resp = supabase.table("uploaded_files").select("*").eq("id", candidate_id).single().execute()
            if resp.data and resp.data.get("analysis_results"):
                candidates_data.append(resp.data["analysis_results"])
        
        if not candidates_data:
            raise HTTPException(status_code=404, detail="No candidate data found")
        
        # Generate comparison matrix
        comparison_result = comparison_matrix.generate_comparison_matrix(
            candidates_data=candidates_data,
            top_n=request.top_n
        )
        
        return ComparisonMatrixResponse(
            comparison_matrix=comparison_result,
            metadata={
                "generated_at": datetime.utcnow().isoformat(),
                "user_id": profile_id,
                "candidates_compared": len(candidates_data),
                "top_n": request.top_n
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

@router.post("/analyze-multiple-candidates")
async def analyze_multiple_candidates(
    request: CandidateComparisonRequest,
    credentials=Depends(bearer_scheme)
):
    """
    Analyze multiple candidates together
    """
    try:
        profile_id = decode_jwt_token(credentials.credentials)
        
        # Get candidate data from database
        candidates_data = []
        for candidate_id in request.candidate_ids:
            resp = supabase.table("uploaded_files").select("*").eq("id", candidate_id).single().execute()
            if resp.data and resp.data.get("analysis_results"):
                candidates_data.append(resp.data["analysis_results"])
        
        if not candidates_data:
            raise HTTPException(status_code=404, detail="No candidate data found")
        
        # Analyze candidates together
        analysis_result = comparison_matrix.analyze_candidates_together(candidates_data)
        
        return {
            "success": True,
            "analysis": analysis_result,
            "metadata": {
                "analyzed_at": datetime.utcnow().isoformat(),
                "user_id": profile_id,
                "candidates_analyzed": len(candidates_data)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/hiring-recommendations")
async def get_hiring_recommendations(
    request: CandidateComparisonRequest,
    credentials=Depends(bearer_scheme)
):
    """
    Get hiring recommendations for candidates
    """
    try:
        profile_id = decode_jwt_token(credentials.credentials)
        
        # Get candidate data from database
        candidates_data = []
        for candidate_id in request.candidate_ids:
            resp = supabase.table("uploaded_files").select("*").eq("id", candidate_id).single().execute()
            if resp.data and resp.data.get("analysis_results"):
                candidates_data.append(resp.data["analysis_results"])
        
        if not candidates_data:
            raise HTTPException(status_code=404, detail="No candidate data found")
        
        # Get hiring recommendations
        recommendations = comparison_matrix.get_hiring_recommendations(candidates_data)
        
        return {
            "success": True,
            "recommendations": recommendations,
            "metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "user_id": profile_id,
                "candidates_analyzed": len(candidates_data)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendations failed: {str(e)}")

@router.get("/summary-report/{user_id}")
async def get_summary_report(
    user_id: str,
    credentials=Depends(bearer_scheme)
):
    """
    Get summary report for all user's candidates
    """
    try:
        profile_id = decode_jwt_token(credentials.credentials)
        
        # Check if user is requesting their own data or has admin access
        if user_id != profile_id and user_id != "me":
            # TODO: Add admin check here if needed
            raise HTTPException(status_code=403, detail="Access denied")
        
        # If user_id is "me", use the profile_id
        target_user_id = profile_id if user_id == "me" else user_id
        
        # Get all candidate data for user
        resp = supabase.table("uploaded_files").select("*").eq("user_id", target_user_id).execute()
        
        candidates_data = []
        all_candidates = []
        requirements_comparison = {}
        key_differentiators = []
        
        for file_data in resp.data:
            if file_data.get("analysis_results"):
                candidate_data = file_data["analysis_results"]
                candidates_data.append(candidate_data)
                
                # Transform candidate data for dashboard
                candidate = {
                    "id": file_data["id"],
                    "full_name": candidate_data.get("full_name", "Unknown"),
                    "score": candidate_data.get("overall_score", 0),
                    "overall_score": candidate_data.get("overall_score", 0),
                    "relevance_percent": candidate_data.get("match_score", 0),
                    "payment": candidate_data.get("salary_expectation", ""),
                    "achievements": len(candidate_data.get("achievements", [])),
                    "skills": len(candidate_data.get("skills", {}).get("technical", [])),
                    "growth": candidate_data.get("career_growth_score", 0),
                    "experience": candidate_data.get("experience_years", 0),
                    "experience_years": candidate_data.get("experience_years", 0),
                    "unique_skills": candidate_data.get("unique_skills", []),
                    "certifications": candidate_data.get("certifications", ""),
                    "education": candidate_data.get("education", []),
                    "specialization": candidate_data.get("specialization", ""),
                    "unique_experience": candidate_data.get("unique_experience", "")
                }
                all_candidates.append(candidate)
        
        if not candidates_data:
            return {
                "candidates": [],
                "requirements_comparison": {},
                "key_differentiators": [],
                "summary": {
                    "total_candidates": 0,
                    "message": "No candidates found for this user"
                }
            }
        
        # Create summary report
        summary = comparison_matrix.create_summary_report(candidates_data)
        requirements_comparison = summary.get("requirements_comparison", {})
        key_differentiators = summary.get("key_differentiators", [])
        
        return {
            "candidates": all_candidates,
            "requirements_comparison": requirements_comparison,
            "key_differentiators": key_differentiators,
            "summary": {
                "total_candidates": len(all_candidates),
                "candidates_analyzed": len(candidates_data),
                "message": f"Found {len(all_candidates)} candidates"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summary report failed: {str(e)}")

@router.get("/candidate-insights/{candidate_id}", response_model=CandidateInsightsResponse)
async def get_candidate_insights(
    candidate_id: str,
    credentials=Depends(bearer_scheme)
):
    """
    Get detailed insights for a specific candidate
    """
    try:
        profile_id = decode_jwt_token(credentials.credentials)
        
        # Get candidate data
        resp = supabase.table("uploaded_files").select("*").eq("id", candidate_id).single().execute()
        
        if not resp.data or not resp.data.get("analysis_results"):
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        candidate_data = resp.data["analysis_results"]
        
        # Get candidate insights
        insights = comparison_matrix.get_candidate_insights(candidate_data)
        
        return CandidateInsightsResponse(
            insights=insights,
            metadata={
                "generated_at": datetime.utcnow().isoformat(),
                "user_id": profile_id,
                "candidate_id": candidate_id
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insights failed: {str(e)}")

@router.post("/export-comparison-csv")
async def export_comparison_csv(
    request: CandidateComparisonRequest,
    credentials=Depends(bearer_scheme)
):
    """
    Export comparison matrix to CSV format
    """
    try:
        profile_id = decode_jwt_token(credentials.credentials)
        
        # Get candidate data from database
        candidates_data = []
        for candidate_id in request.candidate_ids:
            resp = supabase.table("uploaded_files").select("*").eq("id", candidate_id).single().execute()
            if resp.data and resp.data.get("analysis_results"):
                candidates_data.append(resp.data["analysis_results"])
        
        if not candidates_data:
            raise HTTPException(status_code=404, detail="No candidate data found")
        
        # Generate comparison matrix
        comparison_result = comparison_matrix.generate_comparison_matrix(
            candidates_data=candidates_data,
            top_n=request.top_n
        )
        
        # Export to CSV
        csv_data = comparison_matrix.export_comparison_to_csv(comparison_result)
        
        return {
            "success": True,
            "csv_data": csv_data,
            "filename": f"candidate_comparison_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv",
            "metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "user_id": profile_id,
                "candidates_compared": len(candidates_data),
                "top_n": request.top_n
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CSV export failed: {str(e)}")

@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: str,
    credentials=Depends(bearer_scheme)
):
    """
    Get analysis by ID
    """
    try:
        profile_id = decode_jwt_token(credentials.credentials)
        
        # Get analysis from database
        resp = supabase.table("analyses").select("*").eq("id", analysis_id).single().execute()
        
        if not resp.data:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        analysis = resp.data
        
        # Check if user has access to this analysis
        if analysis["user_id"] != profile_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get uploaded files for this analysis
        files_resp = supabase.table("uploaded_files").select("*").eq("analysis_id", analysis_id).execute()
        files = files_resp.data or []
        
        # If analysis is completed, get the results from the first file
        results = None
        if analysis["status"] == "completed" and files:
            # Get results from the first file that has analysis_results
            for file in files:
                if file.get("analysis_results"):
                    results = file["analysis_results"]
                    break
        
        # Format dates
        created_at = analysis.get("created_at", "")
        updated_at = analysis.get("updated_at")
        if isinstance(updated_at, str):
            try:
                updated_at = datetime.fromisoformat(updated_at)
            except Exception:
                updated_at = datetime.utcnow()
        elif updated_at is None:
            updated_at = datetime.utcnow()
        
        return AnalysisResponse(
            id=analysis["id"],
            job_description=analysis["job_description"],
            status=analysis["status"],
            results=results,
            created_at=created_at,
            updated_at=updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analysis: {str(e)}")

@router.post("/{analysis_id}/retry")
async def retry_analysis(
    analysis_id: str,
    credentials=Depends(bearer_scheme)
):
    """
    Retry failed analysis
    """
    try:
        profile_id = decode_jwt_token(credentials.credentials)
        
        # Get analysis from database
        resp = supabase.table("analyses").select("*").eq("id", analysis_id).single().execute()
        
        if not resp.data:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        analysis = resp.data
        
        # Check if user has access to this analysis
        if analysis["user_id"] != profile_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get uploaded files for this analysis
        files_resp = supabase.table("uploaded_files").select("*").eq("analysis_id", analysis_id).execute()
        files = files_resp.data or []
        
        if not files:
            raise HTTPException(status_code=400, detail="No files found for analysis")
        
        # Update status to pending
        supabase.table("analyses").update({"status": "pending"}).eq("id", analysis_id).execute()
        
        # Trigger background analysis
        analyze_cv_background.delay(analysis_id)
        
        return {"success": True, "message": "Analysis retry initiated"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retry analysis: {str(e)}")

@router.post("/{analysis_id}/run")
async def run_analysis(
    analysis_id: str,
    credentials=Depends(bearer_scheme)
):
    """
    Run pending analysis
    """
    try:
        profile_id = decode_jwt_token(credentials.credentials)
        
        # Get analysis from database
        resp = supabase.table("analyses").select("*").eq("id", analysis_id).single().execute()
        
        if not resp.data:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        analysis = resp.data
        
        # Check if user has access to this analysis
        if analysis["user_id"] != profile_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get uploaded files for this analysis
        files_resp = supabase.table("uploaded_files").select("*").eq("analysis_id", analysis_id).execute()
        files = files_resp.data or []
        
        if not files:
            raise HTTPException(status_code=400, detail="No files found for analysis")
        
        # Update status to processing
        supabase.table("analyses").update({"status": "processing"}).eq("id", analysis_id).execute()
        
        # Trigger background analysis
        analyze_cv_background.delay(analysis_id)
        
        return {"success": True, "message": "Analysis started"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run analysis: {str(e)}")

@router.get("/user/me")
async def get_user_analyses(
    credentials=Depends(bearer_scheme)
):
    """
    Get all analyses for the current user
    """
    try:
        profile_id = decode_jwt_token(credentials.credentials)
        
        # Get all analyses for the user
        resp = supabase.table("analyses").select("*").eq("user_id", profile_id).order("created_at", desc=True).execute()
        
        if not resp.data:
            return {
                "analyses": [],
                "total": 0,
                "message": "No analyses found for this user"
            }
        
        # Transform analyses for frontend
        analyses = []
        for analysis in resp.data:
            analysis_data = {
                "id": analysis["id"],
                "job_description": analysis.get("job_description", ""),
                "status": analysis.get("status", "pending"),
                "results": analysis.get("results"),
                "created_at": analysis.get("created_at"),
                "updated_at": analysis.get("updated_at"),
                "processing_time": analysis.get("processing_time", 0)
            }
            analyses.append(analysis_data)
        
        return {
            "analyses": analyses,
            "total": len(analyses),
            "message": f"Found {len(analyses)} analyses"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user analyses: {str(e)}")

@router.get("/summary-report/me")
async def get_summary_report_me(
    credentials=Depends(bearer_scheme)
):
    """
    Get summary report for current user (dashboard compatible)
    """
    try:
        profile_id = decode_jwt_token(credentials.credentials)
        
        # Get all analyses for the user
        resp = supabase.table("analyses").select("*").eq("user_id", profile_id).order("created_at", desc=True).execute()
        
        if not resp.data:
            return {
                "candidates": [],
                "requirements_comparison": {},
                "key_differentiators": [],
                "summary": {
                    "total_candidates": 0,
                    "message": "No analyses found for this user"
                }
            }
        
        # Transform analyses to candidates format for dashboard
        candidates = []
        requirements_comparison = {}
        key_differentiators = []
        
        print(f"Total analyses found: {len(resp.data)}")
        
        for analysis in resp.data:
            print(f"Checking analysis {analysis['id']}: status={analysis.get('status')}, has_results={bool(analysis.get('results'))}")
            print(f"  Status type: {type(analysis.get('status'))}, Status value: '{analysis.get('status')}'")
            print(f"  Results type: {type(analysis.get('results'))}, Results keys: {list(analysis.get('results', {}).keys()) if analysis.get('results') else 'None'}")
            
            if analysis.get("results") and analysis.get("status") == "completed":
                print(f"✅ Processing analysis {analysis['id']} with status {analysis.get('status')} and results: {bool(analysis.get('results'))}")
            else:
                print(f"❌ Skipping analysis {analysis['id']} - condition not met")
                print(f"   Results exists: {bool(analysis.get('results'))}")
                print(f"   Status == 'completed': {analysis.get('status') == 'completed'}")
                print(f"   Status comparison: '{analysis.get('status')}' == 'completed'")
                results = analysis["results"]
                
                # Transform to candidate format using achievers_rating structure
                experience_summary = results.get("experience_summary", {})
                achievers_rating = results.get("achievers_rating", {})
                
                candidate = {
                    "id": analysis["id"],
                    "full_name": experience_summary.get("full_name", "Unknown"),
                    "score": achievers_rating.get("overall_score", 0),
                    "overall_score": achievers_rating.get("overall_score", 0),
                    "relevance_percent": results.get("match_score", 0) * 100,  # Convert to percentage
                    "payment": experience_summary.get("payment_expectations", ""),
                    "achievements": achievers_rating.get("achievements", {}).get("score", 0),
                    "skills": achievers_rating.get("skills", {}).get("score", 0),
                    "growth": achievers_rating.get("responsibilities", {}).get("total_score", 0),
                    "experience": experience_summary.get("years_of_experience", 0),
                    "experience_years": experience_summary.get("years_of_experience", 0),
                    "unique_skills": experience_summary.get("skills_1_plus_years", ""),
                    "certifications": experience_summary.get("certifications", ""),
                    "education": [
                        experience_summary.get("education_degree", ""),
                        experience_summary.get("education_major", ""),
                        experience_summary.get("education_university", "")
                    ],
                    "specialization": experience_summary.get("desired_role", ""),
                    "unique_experience": experience_summary.get("professional_summary", "")
                }
                candidates.append(candidate)
                
                # Add to requirements comparison
                if experience_summary.get("skills_1_plus_years"):
                    skills_list = experience_summary["skills_1_plus_years"].split(",") if isinstance(experience_summary["skills_1_plus_years"], str) else experience_summary["skills_1_plus_years"]
                    for skill in skills_list:
                        skill = skill.strip()
                        if skill and skill not in requirements_comparison:
                            requirements_comparison[skill] = {}
                        if skill:
                            requirements_comparison[skill][experience_summary.get("full_name", "Unknown")] = achievers_rating.get("overall_score", 0)
                
                # Add key differentiators
                if results.get("strengths"):
                    key_differentiators.append(f"{experience_summary.get('full_name', 'Unknown')}: {results.get('strengths', '')[:100]}...")
        
        return {
            "candidates": candidates,
            "requirements_comparison": requirements_comparison,
            "key_differentiators": key_differentiators,
            "summary": {
                "total_candidates": len(candidates),
                "message": f"Found {len(candidates)} completed analyses"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get summary report: {str(e)}")



@router.get("/cv-analysis-status")
async def get_cv_analysis_status():
    """
    Check if the CV analysis system is available
    """
    try:
        # Test if the analyzer can be initialized
        test_analyzer = CVAnalyzer()
        
        return {
            "new_system_available": True,
            "features": {
                "detailed_analysis": True,
                "candidate_comparison": True,
                "achiever_scoring": True,
                "structured_output": True,
                "multiple_candidates_analysis": True,
                "hiring_recommendations": True,
                "summary_reports": True,
                "candidate_insights": True,
                "csv_export": True
            },
            "ai_provider": "Mistral AI",
            "model": os.getenv("MISTRAL_MODEL", "mistral-large-latest"),
            "status": "operational"
        }
    except Exception as e:
        return {
            "new_system_available": False,
            "error": str(e),
            "status": "error"
        } 