"""
Client presence tracking service

Handles tracking of client online/offline status based on polling activity.
Manages last_seen timestamps and determines presence status based on 
configurable thresholds.
"""

from typing import Dict, Optional, List, Tuple
from datetime import datetime, timedelta
from public_tunnel.models.client_presence import (
    ClientPresenceInfo,
    ClientPresenceStatus,
    ClientOfflineStatusInfo,
    OfflineThresholdConfiguration
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
        # US-016: Track when clients went offline for detailed status information
        self._client_offline_timestamps: Dict[str, datetime] = {}
    
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
            # Also clean up offline timestamp tracking
            if key in self._client_offline_timestamps:
                del self._client_offline_timestamps[key]
        
        return len(keys_to_remove)
    
    # US-016: Client Offline Status Management Methods
    
    def get_offline_threshold_configuration(self) -> OfflineThresholdConfiguration:
        """
        Get current offline threshold configuration
        
        Returns:
            Current threshold configuration
        """
        return OfflineThresholdConfiguration(
            offline_threshold_seconds=self.offline_threshold_seconds,
            cleanup_stale_threshold_seconds=3600  # Default 1 hour for cleanup
        )
    
    def update_offline_threshold(self, new_threshold_seconds: int) -> Tuple[int, int]:
        """
        Update offline threshold configuration
        
        Args:
            new_threshold_seconds: New threshold value in seconds
            
        Returns:
            Tuple of (previous_threshold, affected_sessions_count)
        """
        previous_threshold = self.offline_threshold_seconds
        self.offline_threshold_seconds = new_threshold_seconds
        
        # For simplicity, return 1 as affected sessions count (assumes single session scenario)
        # In a real implementation, this would count actual affected sessions
        affected_sessions_count = len(set(info.session_id for info in self._client_presence.values()))
        
        return previous_threshold, affected_sessions_count
    
    def force_offline_status_check_for_session(self, session_id: Optional[str] = None) -> Tuple[int, int, int]:
        """
        Force offline status check for clients in a specific session or all sessions
        
        Args:
            session_id: Optional session ID to limit check scope (None for all sessions)
            
        Returns:
            Tuple of (checked_count, newly_offline_count, already_offline_count)
        """
        now = datetime.now()
        checked_count = 0
        newly_offline_count = 0
        already_offline_count = 0
        
        for presence_key, presence_info in self._client_presence.items():
            # Filter by session if specified
            if session_id and presence_info.session_id != session_id:
                continue
            
            checked_count += 1
            previous_status = presence_info.presence_status
            
            # Recalculate status based on current time
            if presence_info.last_seen_timestamp:
                time_since_last_seen = now - presence_info.last_seen_timestamp
                
                if time_since_last_seen.total_seconds() > self.offline_threshold_seconds:
                    new_status = ClientPresenceStatus.OFFLINE
                    
                    # Track when client went offline
                    if previous_status == ClientPresenceStatus.ONLINE:
                        self._client_offline_timestamps[presence_key] = now
                        newly_offline_count += 1
                    elif previous_status == ClientPresenceStatus.OFFLINE:
                        already_offline_count += 1
                else:
                    new_status = ClientPresenceStatus.ONLINE
                    # Remove offline timestamp if client is back online
                    if presence_key in self._client_offline_timestamps:
                        del self._client_offline_timestamps[presence_key]
            else:
                new_status = ClientPresenceStatus.UNKNOWN
            
            presence_info.presence_status = new_status
        
        return checked_count, newly_offline_count, already_offline_count
    
    def get_detailed_offline_status_for_session(self, session_id: str) -> List[ClientOfflineStatusInfo]:
        """
        Get detailed offline status information for all clients in a session
        
        Args:
            session_id: Session ID to get client status for
            
        Returns:
            List of detailed client offline status information
        """
        now = datetime.now()
        detailed_status_list = []
        
        for presence_key, presence_info in self._client_presence.items():
            if presence_info.session_id != session_id:
                continue
            
            # Calculate seconds since last seen
            seconds_since_last_seen = None
            if presence_info.last_seen_timestamp:
                seconds_since_last_seen = int((now - presence_info.last_seen_timestamp).total_seconds())
            
            # Get offline timestamp if available
            went_offline_at = self._client_offline_timestamps.get(presence_key)
            
            # Determine if client is eligible for commands (only online clients)
            is_eligible_for_commands = (presence_info.presence_status == ClientPresenceStatus.ONLINE)
            
            detailed_info = ClientOfflineStatusInfo(
                client_id=presence_info.client_id,
                session_id=presence_info.session_id,
                presence_status=presence_info.presence_status,
                last_seen_timestamp=presence_info.last_seen_timestamp,
                seconds_since_last_seen=seconds_since_last_seen,
                offline_threshold_seconds=self.offline_threshold_seconds,
                is_eligible_for_commands=is_eligible_for_commands,
                went_offline_at=went_offline_at
            )
            
            detailed_status_list.append(detailed_info)
        
        return detailed_status_list
    
    def get_all_clients_offline_status(self) -> List[ClientOfflineStatusInfo]:
        """
        Get detailed offline status information for all clients across all sessions
        
        Returns:
            List of detailed client offline status information for all clients
        """
        now = datetime.now()
        detailed_status_list = []
        
        for presence_key, presence_info in self._client_presence.items():
            # Calculate seconds since last seen
            seconds_since_last_seen = None
            if presence_info.last_seen_timestamp:
                seconds_since_last_seen = int((now - presence_info.last_seen_timestamp).total_seconds())
            
            # Get offline timestamp if available
            went_offline_at = self._client_offline_timestamps.get(presence_key)
            
            # Determine if client is eligible for commands (only online clients)
            is_eligible_for_commands = (presence_info.presence_status == ClientPresenceStatus.ONLINE)
            
            detailed_info = ClientOfflineStatusInfo(
                client_id=presence_info.client_id,
                session_id=presence_info.session_id,
                presence_status=presence_info.presence_status,
                last_seen_timestamp=presence_info.last_seen_timestamp,
                seconds_since_last_seen=seconds_since_last_seen,
                offline_threshold_seconds=self.offline_threshold_seconds,
                is_eligible_for_commands=is_eligible_for_commands,
                went_offline_at=went_offline_at
            )
            
            detailed_status_list.append(detailed_info)
        
        return detailed_status_list