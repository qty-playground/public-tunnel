"""
Client presence tracking service

Handles tracking of client online/offline status based on polling activity.
Manages last_seen timestamps and determines presence status based on 
configurable thresholds.
"""

from typing import Dict, Optional
from datetime import datetime, timedelta
from public_tunnel.models.client_presence import (
    ClientPresenceInfo,
    ClientPresenceStatus
)


class InMemoryClientPresenceTracker:
    """
    In-memory implementation of client presence tracking
    
    Tracks client presence based on polling activity and configurable
    timeout thresholds. Suitable for development and testing.
    """
    
    def __init__(self, offline_threshold_seconds: int = 60):
        """
        Initialize presence tracker
        
        Args:
            offline_threshold_seconds: Seconds after which client is considered offline
        """
        self.offline_threshold_seconds = offline_threshold_seconds
        self._client_presence: Dict[str, ClientPresenceInfo] = {}
    
    def update_client_last_seen(
        self, 
        client_id: str, 
        session_id: str, 
        timestamp: Optional[datetime] = None
    ) -> ClientPresenceInfo:
        """
        Update client's last seen timestamp and presence status
        
        Args:
            client_id: Unique client identifier
            session_id: Session the client belongs to
            timestamp: Timestamp when client was seen (defaults to now)
            
        Returns:
            Updated client presence information
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # Create composite key for client-session pair
        presence_key = f"{session_id}:{client_id}"
        
        # Get existing presence info or create new
        if presence_key in self._client_presence:
            presence_info = self._client_presence[presence_key]
            presence_info.last_seen_timestamp = timestamp
        else:
            # First time seeing this client
            presence_info = ClientPresenceInfo(
                client_id=client_id,
                session_id=session_id,
                presence_status=ClientPresenceStatus.ONLINE,
                last_seen_timestamp=timestamp,
                first_seen_timestamp=timestamp
            )
        
        # Update presence status based on timestamp
        presence_info.presence_status = self._calculate_presence_status(timestamp)
        
        # Store updated info
        self._client_presence[presence_key] = presence_info
        
        return presence_info
    
    def get_client_presence(self, client_id: str, session_id: str) -> Optional[ClientPresenceInfo]:
        """
        Get current presence information for a client
        
        Args:
            client_id: Unique client identifier
            session_id: Session the client belongs to
            
        Returns:
            Client presence information or None if not found
        """
        presence_key = f"{session_id}:{client_id}"
        presence_info = self._client_presence.get(presence_key)
        
        if presence_info:
            # Update presence status based on current time
            current_status = self._calculate_presence_status(presence_info.last_seen_timestamp)
            presence_info.presence_status = current_status
        
        return presence_info
    
    def _calculate_presence_status(self, last_seen: Optional[datetime]) -> ClientPresenceStatus:
        """
        Calculate presence status based on last seen timestamp
        
        Args:
            last_seen: Last seen timestamp
            
        Returns:
            Current presence status
        """
        if last_seen is None:
            return ClientPresenceStatus.UNKNOWN
        
        time_since_last_seen = datetime.now() - last_seen
        
        if time_since_last_seen.total_seconds() <= self.offline_threshold_seconds:
            return ClientPresenceStatus.ONLINE
        else:
            return ClientPresenceStatus.OFFLINE
    
    def cleanup_stale_clients(self, stale_threshold_seconds: int = 3600) -> int:
        """
        Remove clients that haven't been seen for a very long time
        
        Args:
            stale_threshold_seconds: Seconds after which to remove client records
            
        Returns:
            Number of clients removed
        """
        now = datetime.now()
        keys_to_remove = []
        
        for key, presence_info in self._client_presence.items():
            if presence_info.last_seen_timestamp:
                time_since_last_seen = now - presence_info.last_seen_timestamp
                if time_since_last_seen.total_seconds() > stale_threshold_seconds:
                    keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self._client_presence[key]
        
        return len(keys_to_remove)