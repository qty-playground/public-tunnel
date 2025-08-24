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
    ClientPresenceStatus
)
from public_tunnel.dependencies.providers import (
    SessionRepositoryDep,
    ClientPresenceTrackerDep
)

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