"""
Client offline threshold configuration API router

Handles configuration management for offline status detection thresholds.
Part of US-016: Client Offline Status Management implementation.
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException
from public_tunnel.models.client_presence import (
    OfflineThresholdConfiguration,
    UpdateOfflineThresholdRequest,
    UpdateOfflineThresholdResponse
)
from public_tunnel.dependencies.providers import (
    SessionRepositoryDep,
    ClientPresenceTrackerDep,
    OfflineStatusManagerDep
)

router: APIRouter = APIRouter()


@router.get("/api/configuration/offline-threshold", response_model=OfflineThresholdConfiguration)
async def get_current_offline_threshold_configuration(
    session_repo: SessionRepositoryDep,
    presence_tracker: ClientPresenceTrackerDep,
    offline_status_manager: OfflineStatusManagerDep
) -> OfflineThresholdConfiguration:
    """
    Get current offline threshold configuration
    
    Returns the current configuration for determining when clients 
    should be marked as offline based on polling activity.
    
    US-016: Enables server to manage client offline status thresholds
    """
    # GREEN Stage 2: Real implementation using offline status manager
    return offline_status_manager.get_current_threshold_configuration()


@router.put("/api/configuration/offline-threshold", response_model=UpdateOfflineThresholdResponse)
async def update_offline_threshold_configuration(
    threshold_update: UpdateOfflineThresholdRequest,
    session_repo: SessionRepositoryDep,
    presence_tracker: ClientPresenceTrackerDep,
    offline_status_manager: OfflineStatusManagerDep
) -> UpdateOfflineThresholdResponse:
    """
    Update offline threshold configuration
    
    Updates the time threshold after which clients are considered offline
    if they haven't sent polling requests. This affects all future 
    offline status determinations.
    
    US-016: Allows configuration of client offline detection thresholds
    """
    # GREEN Stage 2: Real implementation using offline status manager
    previous_threshold, current_threshold, affected_sessions_count = (
        offline_status_manager.update_threshold_configuration(threshold_update.offline_threshold_seconds)
    )
    
    return UpdateOfflineThresholdResponse(
        previous_threshold_seconds=previous_threshold,
        current_threshold_seconds=current_threshold,
        updated_at=datetime.now(),
        affected_sessions_count=affected_sessions_count
    )