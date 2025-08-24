"""
Command - 指令資料結構

基於 OOA 設計的指令資料和狀態管理
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class CommandExecutionStatus(str, Enum):
    """指令執行狀態列舉"""
    PENDING = "pending"
    RUNNING = "running" 
    COMPLETED = "completed"
    FAILED = "failed"


class SubmitCommandToTargetClientRequest(BaseModel):
    """提交指令給目標 Client 的請求模型"""
    command_content: str
    target_client_id: str
    timeout_seconds: Optional[int] = None


class CommandSubmissionToTargetResponse(BaseModel):
    """指令提交給目標 Client 的回應模型"""
    command_id: str
    execution_status: CommandExecutionStatus
    submission_timestamp: datetime
    target_client_id: str
    estimated_completion_time: Optional[datetime] = None


class CommandExecutionStatusResponse(BaseModel):
    """指令執行狀態查詢回應模型"""
    command_id: str
    execution_status: CommandExecutionStatus
    client_id: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result_summary: Optional[str] = None
    error_message: Optional[str] = None


class ClientCommandRetrievalResponse(BaseModel):
    """US-009: Client 單一指令接收回應模型"""
    session_id: str
    client_id: str
    command: Optional[dict] = None  # 單一指令，格式與現有相容
    has_more_commands: bool = False  # 是否還有更多指令
    queue_size: int = 0  # 剩餘佇列大小


class Command:
    """指令資料結構 - 基於 OOA 設計"""
    
    def __init__(self, command_id: str, content: str, target_client: str, session_id: str):
        self.command_id = command_id
        self.content = content
        self.target_client = target_client
        self.session_id = session_id
        self.timestamp = datetime.now().timestamp()
    
    def get_target_client(self) -> str:
        """取得目標 Client"""
        return self.target_client
    
    def get_age(self) -> int:
        """取得指令年齡（秒）"""
        return int(datetime.now().timestamp() - self.timestamp)
    
    def to_json(self) -> dict:
        """序列化為 JSON"""
        return {
            "command_id": self.command_id,
            "content": self.content,
            "target_client": self.target_client,
            "session_id": self.session_id,
            "timestamp": self.timestamp
        }