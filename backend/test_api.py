#!/usr/bin/env python3
"""
API Tests for NoaMetrics Backend
================================

Automated tests for all API endpoints using pytest and httpx.
"""

import pytest
import httpx
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test@example.com"
TEST_NAME = "Test User"
TEST_PHONE = "+1234567890"

@pytest.fixture
async def client():
    """Create async HTTP client for testing."""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        yield client

@pytest.fixture
async def auth_token(client):
    """Get authentication token for testing protected endpoints."""
    # Register/join beta to get token
    response = await client.post("/join-beta", json={
        "email": TEST_EMAIL,
        "name": TEST_NAME,
        "phone": TEST_PHONE
    })
    assert response.status_code == 200
    data = response.json()
    return data["access_token"]

class TestPublicEndpoints:
    """Test public endpoints that don't require authentication."""
    
    async def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "NoaMetrics Backend API"
    
    async def test_join_beta_success(self, client):
        """Test successful user registration."""
        response = await client.post("/join-beta", json={
            "email": "newuser@example.com",
            "name": "New User",
            "phone": "+1234567891"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
    
    async def test_join_beta_invalid_email(self, client):
        """Test user registration with invalid email."""
        response = await client.post("/join-beta", json={
            "email": "invalid-email",
            "name": "Test User",
            "phone": "+1234567890"
        })
        assert response.status_code == 422  # Validation error
    
    async def test_join_beta_missing_fields(self, client):
        """Test user registration with missing required fields."""
        response = await client.post("/join-beta", json={
            "email": "test@example.com"
            # Missing name and phone
        })
        assert response.status_code == 422  # Validation error

class TestAuthenticatedEndpoints:
    """Test endpoints that require authentication."""
    
    async def test_me_endpoint(self, client, auth_token):
        """Test getting current user profile."""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = await client.get("/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "email" in data
        assert "name" in data
    
    async def test_me_endpoint_no_token(self, client):
        """Test getting user profile without token."""
        response = await client.get("/me")
        assert response.status_code == 403  # Forbidden
    
    async def test_me_endpoint_invalid_token(self, client):
        """Test getting user profile with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = await client.get("/me", headers=headers)
        assert response.status_code == 401  # Unauthorized
    
    async def test_my_upload_limit(self, client, auth_token):
        """Test getting user upload limits."""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = await client.get("/my-upload-limit", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "analysis_count" in data
        assert "max_weekly_analyses" in data
        assert "week_start" in data
    
    async def test_my_uploads_empty(self, client, auth_token):
        """Test getting user uploads when none exist."""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = await client.get("/my-uploads", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    async def test_my_analyses_empty(self, client, auth_token):
        """Test getting user analyses when none exist."""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = await client.get("/my-analyses", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

class TestAnalysisEndpoints:
    """Test analysis-related endpoints."""
    
    async def test_create_analysis(self, client, auth_token):
        """Test creating a new analysis."""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = await client.post("/create-analysis", 
                                   json={"job_description": "Test job description"},
                                   headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "analysis_id" in data
    
    async def test_create_analysis_no_job_description(self, client, auth_token):
        """Test creating analysis without job description."""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = await client.post("/create-analysis", 
                                   json={},
                                   headers=headers)
        assert response.status_code == 422  # Validation error
    
    async def test_compare_candidates(self, client, auth_token):
        """Test comparing candidates endpoint."""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = await client.get("/compare-candidates", headers=headers)
        assert response.status_code == 200
        data = response.json()
        # Should return comparison data structure
        assert isinstance(data, dict)

class TestFileUploadEndpoints:
    """Test file upload endpoints."""
    
    async def test_upload_file_no_analysis_id(self, client, auth_token):
        """Test file upload without analysis_id."""
        headers = {"Authorization": f"Bearer {auth_token}"}
        files = {"file": ("test.pdf", b"fake pdf content", "application/pdf")}
        response = await client.post("/upload", files=files, headers=headers)
        assert response.status_code == 422  # Missing analysis_id
    
    async def test_upload_file_invalid_type(self, client, auth_token):
        """Test file upload with invalid file type."""
        headers = {"Authorization": f"Bearer {auth_token}"}
        files = {"file": ("test.txt", b"text content", "text/plain")}
        data = {"analysis_id": "test-analysis-id"}
        response = await client.post("/upload", files=files, data=data, headers=headers)
        assert response.status_code == 400  # Invalid file type

class TestErrorHandling:
    """Test error handling and edge cases."""
    
    async def test_nonexistent_endpoint(self, client):
        """Test accessing non-existent endpoint."""
        response = await client.get("/nonexistent")
        assert response.status_code == 404
    
    async def test_method_not_allowed(self, client):
        """Test using wrong HTTP method."""
        response = await client.post("/")  # GET endpoint
        assert response.status_code == 405  # Method Not Allowed
    
    async def test_cv_analysis_status(self, client):
        """Test CV analysis status endpoint."""
        response = await client.get("/cv-analysis-status")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data

# Integration tests
class TestIntegration:
    """Integration tests for complete workflows."""
    
    async def test_complete_analysis_workflow(self, client):
        """Test complete analysis workflow from registration to results."""
        # 1. Register user
        register_response = await client.post("/join-beta", json={
            "email": "workflow@example.com",
            "name": "Workflow User",
            "phone": "+1234567892"
        })
        assert register_response.status_code == 200
        token = register_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Check upload limits
        limits_response = await client.get("/my-upload-limit", headers=headers)
        assert limits_response.status_code == 200
        
        # 3. Create analysis
        analysis_response = await client.post("/create-analysis", 
                                            json={"job_description": "Integration test job"},
                                            headers=headers)
        assert analysis_response.status_code == 200
        analysis_id = analysis_response.json()["analysis_id"]
        
        # 4. Check analyses list
        analyses_response = await client.get("/my-analyses", headers=headers)
        assert analyses_response.status_code == 200

if __name__ == "__main__":
    # Run tests with pytest
    import sys
    import subprocess
    
    print("🧪 Running API Tests...")
    print("=" * 50)
    
    # Check if backend is running
    try:
        response = httpx.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("❌ Backend is not running. Please start the backend first:")
            print("   cd backend && uvicorn main:app --reload")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Cannot connect to backend at {BASE_URL}")
        print("   Please start the backend first: cd backend && uvicorn main:app --reload")
        sys.exit(1)
    
    print("✅ Backend is running")
    
    # Run pytest
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        __file__, 
        "-v", 
        "--asyncio-mode=auto"
    ])
    
    sys.exit(result.returncode) 