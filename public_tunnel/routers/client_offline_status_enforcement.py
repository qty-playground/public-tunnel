"""
Client offline status enforcement API router

Handles forced offline status checking and enforcement functionality.
Part of US-016: Client Offline Status Management implementation.
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException
from public_tunnel.models.client_presence import (
    ForceOfflineStatusCheckRequest,
    ForceOfflineStatusCheckResponse,
    ClientOfflineStatusInfo
)
from public_tunnel.dependencies.providers import (
    SessionRepositoryDep,
    ClientPresenceTrackerDep,
    OfflineStatusManagerDep
)
from typing import List

router: APIRouter = APIRouter()


@router.post("/api/sessions/{session_id}/clients/force-offline-check", response_model=ForceOfflineStatusCheckResponse)
async def force_offline_status_check_for_session(
    session_id: str,
    check_request: ForceOfflineStatusCheckRequest,
    session_repo: SessionRepositoryDep,
    presence_tracker: ClientPresenceTrackerDep,
    offline_status_manager: OfflineStatusManagerDep
) -> ForceOfflineStatusCheckResponse:
    """
    Force offline status check for all clients in a specific session
    
    Immediately evaluates all clients in the session against the configured 
    offline threshold and marks clients as offline if they haven't polled 
    within the threshold period.
    
    US-016: Enables forced offline status checking for session-specific clients
    """
    # GREEN Stage 2: Real implementation using offline status manager
    return offline_status_manager.execute_force_offline_check_for_session(session_id)


@router.post("/api/admin/clients/force-offline-check", response_model=ForceOfflineStatusCheckResponse)
async def force_offline_status_check_for_all_sessions(
    check_request: ForceOfflineStatusCheckRequest,
    session_repo: SessionRepositoryDep,
    presence_tracker: ClientPresenceTrackerDep,
    offline_status_manager: OfflineStatusManagerDep
) -> ForceOfflineStatusCheckResponse:
    """
    Force offline status check across all sessions
    
    Immediately evaluates all clients across all sessions against the 
    configured offline threshold and marks clients as offline if they 
    haven't polled within the threshold period.
    
    US-016: Enables system-wide forced offline status checking
    """
    # GREEN Stage 2: Real implementation using offline status manager
    return offline_status_manager.execute_force_offline_check_for_all_sessions()


@router.get("/api/sessions/{session_id}/clients/offline-status", response_model=List[ClientOfflineStatusInfo])
async def get_detailed_offline_status_for_session_clients(
    session_id: str,
    session_repo: SessionRepositoryDep,
    presence_tracker: ClientPresenceTrackerDep,
    offline_status_manager: OfflineStatusManagerDep
) -> List[ClientOfflineStatusInfo]:
    """
    Get detailed offline status information for all clients in a session
    
    Returns comprehensive offline status details including time since last seen,
    eligibility for receiving commands, and offline threshold information.
    
    US-016: Provides detailed offline status information for monitoring and debugging
    """
    # GREEN Stage 2: Real implementation using offline status manager
    return offline_status_manager.get_detailed_offline_status_for_session(session_id)