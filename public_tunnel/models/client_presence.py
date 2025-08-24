"""
Client presence tracking models for public tunnel API

Contains Pydantic models related to client presence and status management.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class ClientPresenceStatus(str, Enum):
    """Client presence status enumeration"""
    ONLINE = "online"
    OFFLINE = "offline"
    UNKNOWN = "unknown"


class ClientPresenceInfo(BaseModel):
    """Information about client presence status"""
    client_id: str = Field(description="Unique identifier for the client")
    session_id: str = Field(description="Session ID the client belongs to")
    presence_status: ClientPresenceStatus = Field(description="Current presence status")
    last_seen_timestamp: Optional[datetime] = Field(
        default=None,
        description="Last time the client was seen (via polling)"
    )
    first_seen_timestamp: Optional[datetime] = Field(
        default=None, 
        description="First time the client was registered"
    )
    heartbeat_interval_seconds: Optional[int] = Field(
        default=30,
        description="Expected heartbeat interval in seconds"
    )


class UpdateClientPresenceRequest(BaseModel):
    """Request to update client presence information"""
    client_id: str = Field(description="Unique identifier for the client")
    last_seen_timestamp: datetime = Field(description="Timestamp when client was last seen")


class UpdateClientPresenceResponse(BaseModel):
    """Response after updating client presence"""
    client_id: str = Field(description="Client ID that was updated")
    session_id: str = Field(description="Session ID the client belongs to") 
    previous_status: ClientPresenceStatus = Field(description="Previous presence status")
    current_status: ClientPresenceStatus = Field(description="Updated presence status")
    last_seen_timestamp: datetime = Field(description="Updated last seen timestamp")
    updated_at: datetime = Field(description="When this update occurred")


class ClientPresenceQueryResponse(BaseModel):
    """Response for querying client presence information"""
    client_id: str = Field(description="Client ID being queried")
    session_id: str = Field(description="Session ID the client belongs to")
    presence_status: ClientPresenceStatus = Field(description="Current presence status")
    last_seen_timestamp: Optional[datetime] = Field(
        default=None,
        description="Last time the client was seen"
    )
    online_duration_seconds: Optional[int] = Field(
        default=None,
        description="How long client has been online in seconds"
    )


# US-016: Client Offline Status Management Models

class OfflineThresholdConfiguration(BaseModel):
    """Configuration for client offline status detection threshold"""
    offline_threshold_seconds: int = Field(
        default=60,
        ge=1,
        le=3600,
        description="Seconds after which client is marked offline (1 sec to 1 hour)"
    )
    cleanup_stale_threshold_seconds: int = Field(
        default=3600,
        ge=60,
        description="Seconds after which stale client records are cleaned up (min 1 minute)"
    )


class UpdateOfflineThresholdRequest(BaseModel):
    """Request to update offline threshold configuration"""
    offline_threshold_seconds: int = Field(
        ge=1,
        le=3600,
        description="New offline threshold in seconds (1 sec to 1 hour)"
    )


class UpdateOfflineThresholdResponse(BaseModel):
    """Response after updating offline threshold configuration"""
    previous_threshold_seconds: int = Field(description="Previous threshold value")
    current_threshold_seconds: int = Field(description="Updated threshold value")
    updated_at: datetime = Field(description="When this configuration update occurred")
    affected_sessions_count: int = Field(
        default=0,
        description="Number of sessions affected by this threshold change"
    )


class ForceOfflineStatusCheckRequest(BaseModel):
    """Request to force offline status check across all clients"""
    session_id: Optional[str] = Field(
        default=None,
        description="Optional session ID to limit check scope (all sessions if None)"
    )


class ForceOfflineStatusCheckResponse(BaseModel):
    """Response after forcing offline status check"""
    checked_clients_count: int = Field(description="Total number of clients checked")
    newly_offline_clients_count: int = Field(description="Number of clients newly marked offline")
    already_offline_clients_count: int = Field(description="Number of clients already offline")
    session_id: Optional[str] = Field(
        default=None,
        description="Session ID if check was limited to specific session"
    )
    check_timestamp: datetime = Field(description="When the status check was performed")


class ClientOfflineStatusInfo(BaseModel):
    """Extended client information including offline status details"""
    client_id: str = Field(description="Client unique identifier")
    session_id: str = Field(description="Session the client belongs to")
    presence_status: ClientPresenceStatus = Field(description="Current presence status")
    last_seen_timestamp: Optional[datetime] = Field(
        default=None,
        description="Last time client was seen"
    )
    seconds_since_last_seen: Optional[int] = Field(
        default=None,
        description="Seconds elapsed since last seen (None if never seen)"
    )
    offline_threshold_seconds: int = Field(description="Configured offline threshold")
    is_eligible_for_commands: bool = Field(description="Whether client can receive new commands")
    went_offline_at: Optional[datetime] = Field(
        default=None,
        description="When client was first marked as offline (None if online)"
    )