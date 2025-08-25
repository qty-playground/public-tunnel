"""
File Manager Service for US-010: AI File Upload Feature

Manages file upload, storage, and download with session-based isolation.
Supports Base64 encoding/decoding for web API compatibility.
"""

from typing import Dict, List, Optional
import base64
import threading
from datetime import datetime
from public_tunnel.models.file import File, FileUploadRequest, FileUploadResponse, FileDownloadResponse, SessionFileListResponse


class FileManager:
    """
    Manages file storage and retrieval with session-based isolation
    
    Features:
    - Session-based file isolation
    - Base64 encoding/decoding for web compatibility
    - Thread-safe operations
    - Unique file ID generation
    """
    
    def __init__(self):
        """Initialize empty file manager"""
        # Structure: {session_id: {file_id: File}}
        self._session_files: Dict[str, Dict[str, File]] = {}
        self._lock = threading.RLock()
    
    def upload_file_to_session(
        self, 
        session_id: str, 
        file_request: FileUploadRequest
    ) -> FileUploadResponse:
        """
        Upload file to specific session
        
        Args:
            session_id: Target session identifier
            file_request: File upload request with Base64 content
            
        Returns:
            FileUploadResponse: Upload response with unique file-id
            
        Raises:
            ValueError: If Base64 decoding fails
        """
        with self._lock:
            # Decode Base64 content
            try:
                file_content = base64.b64decode(file_request.file_content_base64)
            except Exception as e:
                raise ValueError(f"Invalid Base64 content: {str(e)}")
            
            # Create File object
            file_obj = File(
                file_name=file_request.file_name,
                content=file_content,
                session_id=session_id,
                content_type=file_request.content_type,
                file_summary=file_request.file_summary
            )
            
            # Ensure session exists
            if session_id not in self._session_files:
                self._session_files[session_id] = {}
            
            # Store file
            file_id = file_obj.get_unique_id()
            self._session_files[session_id][file_id] = file_obj
            
            # Return upload response
            return FileUploadResponse(
                file_id=file_id,
                file_name=file_obj.file_name,
                session_id=session_id,
                upload_timestamp=datetime.fromtimestamp(file_obj.created_time),
                file_size_bytes=file_obj.get_size(),
                content_type=file_obj.content_type,
                file_summary=file_obj.file_summary
            )
    
    def download_file_from_session(
        self, 
        session_id: str, 
        file_id: str
    ) -> Optional[FileDownloadResponse]:
        """
        Download file from specific session
        
        Args:
            session_id: Target session identifier
            file_id: File unique identifier
            
        Returns:
            FileDownloadResponse: Download response with Base64 content, or None if not found
        """
        with self._lock:
            if session_id not in self._session_files:
                return None
                
            if file_id not in self._session_files[session_id]:
                return None
            
            file_obj = self._session_files[session_id][file_id]
            
            # Verify session ownership
            if not file_obj.belongs_to_session(session_id):
                return None
            
            # Encode content to Base64
            file_content_base64 = base64.b64encode(file_obj.content).decode('utf-8')
            
            return FileDownloadResponse(
                file_id=file_id,
                file_name=file_obj.file_name,
                file_content_base64=file_content_base64,
                content_type=file_obj.content_type,
                file_size_bytes=file_obj.get_size(),
                upload_timestamp=datetime.fromtimestamp(file_obj.created_time),
                file_summary=file_obj.file_summary
            )
    
    def list_session_files(
        self, 
        session_id: str
    ) -> SessionFileListResponse:
        """
        List all files in specific session
        
        Args:
            session_id: Target session identifier
            
        Returns:
            SessionFileListResponse: Session file list with metadata
        """
        with self._lock:
            if session_id not in self._session_files:
                return SessionFileListResponse(
                    session_id=session_id,
                    total_files=0,
                    files=[]
                )
            
            session_files = self._session_files[session_id]
            file_metadata_list = []
            
            for file_obj in session_files.values():
                file_metadata_list.append(file_obj.to_metadata_response())
            
            return SessionFileListResponse(
                session_id=session_id,
                total_files=len(file_metadata_list),
                files=file_metadata_list
            )
    
    def file_exists_in_session(
        self, 
        session_id: str, 
        file_id: str
    ) -> bool:
        """
        Check if file exists in specific session
        
        Args:
            session_id: Target session identifier
            file_id: File unique identifier
            
        Returns:
            bool: True if file exists in session
        """
        with self._lock:
            if session_id not in self._session_files:
                return False
                
            return file_id in self._session_files[session_id]
    
    def clear_session_files(self, session_id: str) -> None:
        """
        Clear all files for a session
        
        Args:
            session_id: Session identifier to clear
        """
        with self._lock:
            if session_id in self._session_files:
                del self._session_files[session_id]
    
    def get_file_count_in_session(self, session_id: str) -> int:
        """
        Get number of files in specific session
        
        Args:
            session_id: Target session identifier
            
        Returns:
            int: Number of files in session
        """
        with self._lock:
            if session_id not in self._session_files:
                return 0
                
            return len(self._session_files[session_id])
    
    def get_file_info(self, file_id: str) -> Optional[File]:
        """
        Get file information by file ID across all sessions
        
        Args:
            file_id: File unique identifier
            
        Returns:
            File: File object if found, None otherwise
            
        Note: Used by SessionFileAccessValidator to validate file ownership
        """
        with self._lock:
            for session_id, session_files in self._session_files.items():
                if file_id in session_files:
                    return session_files[file_id]
            return None


class InMemoryFileManager(FileManager):
    """In-memory implementation of FileManager for development/testing"""
    pass