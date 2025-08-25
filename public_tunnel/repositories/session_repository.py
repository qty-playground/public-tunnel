"""
Session Repository - 管理 session 資料的儲存和檢索

實作 US-003: Default Session Auto Join 所需的 session 管理功能
"""

from typing import Dict, Set, Optional
from datetime import datetime
from public_tunnel.models.session import SessionInfo


class InMemorySessionRepository:
    """
    記憶體內的 Session Repository 實作
    
    用於 TDD 開發和測試，在實際部署時可替換為資料庫實作
    """
    
    def __init__(self):
        # Session ID -> SessionInfo mapping
        self._sessions: Dict[str, SessionInfo] = {}
        # Session ID -> Set of Client IDs mapping 
        self._session_clients: Dict[str, Set[str]] = {}
        
        # Initialize default session
        self._ensure_default_session_exists()
    
    def _ensure_default_session_exists(self) -> None:
        """確保預設 session 存在"""
        default_session_id = "default"
        if default_session_id not in self._sessions:
            self._sessions[default_session_id] = SessionInfo(
                session_id=default_session_id,
                client_count=0,
                created_at=datetime.now(),
                default_session=True
            )
            self._session_clients[default_session_id] = set()
    
    def get_default_session_id(self) -> str:
        """獲取預設 session ID"""
        return "default"
    
    def get_session_info(self, session_id: str) -> Optional[SessionInfo]:
        """獲取 session 資訊"""
        return self._sessions.get(session_id)
    
    def add_client_to_session(self, session_id: str, client_id: str) -> bool:
        """
        將 client 加入到 session
        
        Returns:
            bool: True if client was newly added, False if already existed
        """
        self._ensure_default_session_exists()
        
        # US-004: Create session if it doesn't exist (for specified session collaboration)
        if session_id not in self._sessions:
            self._sessions[session_id] = SessionInfo(
                session_id=session_id,
                client_count=0,
                created_at=datetime.now(),
                default_session=(session_id == "default")
            )
        
        if session_id not in self._session_clients:
            self._session_clients[session_id] = set()
        
        is_new_client = client_id not in self._session_clients[session_id]
        self._session_clients[session_id].add(client_id)
        
        # Update client count in session info
        if session_id in self._sessions:
            self._sessions[session_id].client_count = len(self._session_clients[session_id])
        
        return is_new_client
    
    def is_client_in_session(self, session_id: str, client_id: str) -> bool:
        """檢查 client 是否已在 session 中"""
        if session_id not in self._session_clients:
            return False
        return client_id in self._session_clients[session_id]
    
    def get_clients_in_session(self, session_id: str) -> Set[str]:
        """獲取 session 中的所有 client IDs"""
        return self._session_clients.get(session_id, set()).copy()
    
    def get_all_sessions(self) -> list[SessionInfo]:
        """
        US-001: Get all sessions for admin query
        
        Returns:
            list[SessionInfo]: List of all sessions in the system
        """
        return list(self._sessions.values())