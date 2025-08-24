"""
Client presence tracking API router

Handles client presence tracking functionality including updating last_seen timestamps
and managing online/offline status based on polling activity.
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException
from public_tunnel.models.client_presence import (
    UpdateClientPresenceRequest,
    UpdateClientPresenceResponse, 
    ClientPresenceQueryResponse,
    ClientPresenceStatus,
    ClientOfflineStatusInfo
)
from public_tunnel.dependencies.providers import (
    SessionRepositoryDep,
    ClientPresenceTrackerDep,
    OfflineStatusManagerDep
)
from typing import List, Optional
from fastapi import Query

router: APIRouter = APIRouter()


@router.post("/api/sessions/{session_id}/clients/{client_id}/presence", response_model=UpdateClientPresenceResponse)
async def update_client_presence_in_session(
    session_id: str,
    client_id: str,
    presence_request: UpdateClientPresenceRequest,
    session_repo: SessionRepositoryDep,
    presence_tracker: ClientPresenceTrackerDep
) -> UpdateClientPresenceResponse:
    """
    Update client presence information when client polls the server
    
    This endpoint is called to update the client's last_seen timestamp
    and maintain accurate online/offline status tracking.
    """
    # Get previous presence info to determine status change  
    previous_presence_info = presence_tracker.get_client_presence(client_id, session_id)
    previous_status = previous_presence_info.presence_status if previous_presence_info else ClientPresenceStatus.UNKNOWN

    # Update client presence using the tracker service
    updated_presence_info = presence_tracker.update_client_last_seen(
        client_id=client_id,
        session_id=session_id,
        timestamp=presence_request.last_seen_timestamp
    )

    # Determine current status based on the update
    current_status = updated_presence_info.presence_status

    # Prepare the response
    return UpdateClientPresenceResponse(
        client_id=client_id,
        session_id=session_id,
        previous_status=previous_status,
        current_status=current_status,
        last_seen_timestamp=updated_presence_info.last_seen_timestamp,
        updated_at=datetime.utcnow() # Use current time for update timestamp
    )


@router.get("/api/sessions/{session_id}/clients/{client_id}/presence", response_model=ClientPresenceQueryResponse)
async def get_client_presence_status_from_session(
    session_id: str,
    client_id: str,
    session_repo: SessionRepositoryDep,
    presence_tracker: ClientPresenceTrackerDep
) -> ClientPresenceQueryResponse:
    """
    Query current presence status of a specific client
    
    Returns the current online/offline status and last_seen information
    for the specified client in the given session.
    """
    # Get client presence information
    presence_info = presence_tracker.get_client_presence(client_id, session_id)
    
    if not presence_info:
        raise HTTPException(
            status_code=404,
            detail=f"Client {client_id} not found in session {session_id}"
        )
    
    # Calculate online duration if client is online
    online_duration_seconds = None
    if (presence_info.presence_status == "online" and 
        presence_info.first_seen_timestamp and 
        presence_info.last_seen_timestamp):
        
        duration = presence_info.last_seen_timestamp - presence_info.first_seen_timestamp
        online_duration_seconds = int(duration.total_seconds())
    
    return ClientPresenceQueryResponse(
        client_id=client_id,
        session_id=session_id,
        presence_status=presence_info.presence_status,
        last_seen_timestamp=presence_info.last_seen_timestamp,
        online_duration_seconds=online_duration_seconds
    )


# US-016: Enhanced client presence querying with offline status filtering

@router.get("/api/sessions/{session_id}/clients/presence", response_model=List[ClientOfflineStatusInfo])
async def get_all_clients_presence_status_in_session(
    session_id: str,
    session_repo: SessionRepositoryDep,
    presence_tracker: ClientPresenceTrackerDep,
    offline_status_manager: OfflineStatusManagerDep,
    status_filter: Optional[ClientPresenceStatus] = Query(
        default=None,
        description="Optional filter by presence status (online/offline/unknown)"
    )
) -> List[ClientOfflineStatusInfo]:
    """
    Get presence status for all clients in a session with optional status filtering
    
    Returns detailed offline status information for all clients in the specified session.
    Supports filtering by presence status to show only online, offline, or unknown clients.
    
    US-016: Enhanced presence querying with detailed offline status and filtering support
    """
    # API Skeleton stage: Return 501 Not Implemented
    raise HTTPException(
        status_code=501,
        detail="Get all clients presence status in session not implemented yet"
    )


@router.get("/api/sessions/{session_id}/clients/eligible-for-commands", response_model=List[ClientOfflineStatusInfo])
async def get_clients_eligible_for_commands_in_session(
    session_id: str,
    session_repo: SessionRepositoryDep,
    presence_tracker: ClientPresenceTrackerDep,
    offline_status_manager: OfflineStatusManagerDep
) -> List[ClientOfflineStatusInfo]:
    """
    Get all clients in session that are eligible to receive commands
    
    Returns only clients that are online and can receive new commands.
    This is the core filtering for US-016 - offline clients cannot receive commands.
    
    US-016: Command eligibility filtering based on offline status management
    """
    # API Skeleton stage: Return 501 Not Implemented
    raise HTTPException(
        status_code=501,
        detail="Get clients eligible for commands in session not implemented yet"
    )