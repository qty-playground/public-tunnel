"""
ExecutionResult - 執行結果資料結構

基於 OOA 設計的執行結果資料
"""

from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from public_tunnel.models.file import ClientResultFileUploadRequest, ClientResultFileUploadResponse


class CommandExecutionMode(str, Enum):
    """指令執行模式列舉 - US-021 統一處理"""
    SYNC = "sync"
    ASYNC = "async"


class ExecutionResultStatus(str, Enum):
    """執行結果狀態列舉"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class UnifiedResultQueryResponse(BaseModel):
    """US-021: 統一結果查詢回應模型"""
    command_id: str
    execution_mode: CommandExecutionMode  # 區分是 sync 還是 async 模式
    execution_status: ExecutionResultStatus
    client_id: str
    session_id: str
    submitted_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result_content: Optional[str] = None
    error_message: Optional[str] = None
    file_references: Optional[List[str]] = None  # 附件檔案ID列表


class ExecutionResultSubmissionRequest(BaseModel):
    """執行結果提交請求模型"""
    command_id: str
    execution_status: ExecutionResultStatus
    result_content: Optional[str] = None
    error_message: Optional[str] = None
    execution_duration_seconds: Optional[int] = None
    file_references: Optional[List[str]] = None


class ExecutionResult:
    """執行結果資料結構 - 基於 OOA 設計"""
    
    def __init__(self, command_id: str, execution_status: ExecutionResultStatus, 
                 client_id: str, session_id: str, execution_mode: CommandExecutionMode):
        self.command_id = command_id
        self.execution_status = execution_status
        self.client_id = client_id
        self.session_id = session_id
        self.execution_mode = execution_mode
        self.submitted_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.result_content: Optional[str] = None
        self.error_message: Optional[str] = None
        self.file_references: List[str] = []
    
    def get_command_id(self) -> str:
        """取得指令ID"""
        return self.command_id
    
    def get_execution_status(self) -> ExecutionResultStatus:
        """取得執行狀態"""
        return self.execution_status
    
    def update_status_to_running(self) -> None:
        """更新狀態為執行中"""
        self.execution_status = ExecutionResultStatus.RUNNING
        self.started_at = datetime.now()
    
    def complete_with_success(self, result_content: str, file_references: List[str] = None) -> None:
        """完成執行並設定成功結果"""
        self.execution_status = ExecutionResultStatus.COMPLETED
        self.completed_at = datetime.now()
        self.result_content = result_content
        self.file_references = file_references or []
    
    def complete_with_failure(self, error_message: str) -> None:
        """完成執行並設定失敗結果"""
        self.execution_status = ExecutionResultStatus.FAILED
        self.completed_at = datetime.now()
        self.error_message = error_message
    
    def to_unified_response(self) -> UnifiedResultQueryResponse:
        """轉換為統一查詢回應格式 - US-021 核心功能"""
        return UnifiedResultQueryResponse(
            command_id=self.command_id,
            execution_mode=self.execution_mode,
            execution_status=self.execution_status,
            client_id=self.client_id,
            session_id=self.session_id,
            submitted_at=self.submitted_at,
            started_at=self.started_at,
            completed_at=self.completed_at,
            result_content=self.result_content,
            error_message=self.error_message,
            file_references=self.file_references
        )