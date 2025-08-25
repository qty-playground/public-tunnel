"""
US-001: Admin Session List Query router

Provides admin endpoints to list all sessions in the system.
Requires admin token authentication via Authorization header.
"""

from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from datetime import datetime
from public_tunnel.models.session import AdminSessionListResponse
from public_tunnel.dependencies.providers import (
    SessionRepositoryDep,
    AdminTokenValidatorDep
)

router = APIRouter()


@router.get("/api/sessions", response_model=AdminSessionListResponse)
async def list_all_sessions_for_admin_management(
    session_repo: SessionRepositoryDep,
    admin_validator: AdminTokenValidatorDep,
    authorization: Optional[str] = Header(None)
) -> AdminSessionListResponse:
    """
    List all sessions in the system (admin only)
    
    Requires valid admin token in Authorization header.
    Returns comprehensive list of all sessions with metadata.
    
    Args:
        session_repo: Session repository for data access
        admin_validator: Admin token validator service  
        authorization: Authorization header containing admin token
        
    Returns:
        AdminSessionListResponse: List of all sessions with metadata
        
    Raises:
        HTTPException: 403 if token is invalid/missing
    """
    # GREEN Stage 2: Real implementation with admin token validation
    
    # Validate admin token
    if not admin_validator.is_admin_request(authorization):
        raise HTTPException(
            status_code=403,
            detail="Admin token required for session list access"
        )
    
    # Get all sessions from repository
    all_sessions = session_repo.get_all_sessions()
    
    return AdminSessionListResponse(
        sessions=all_sessions,
        total_sessions=len(all_sessions),
        queried_at=datetime.now()
    )