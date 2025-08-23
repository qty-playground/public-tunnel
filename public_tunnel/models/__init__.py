"""
Public-Tunnel Core Models

Core data structures and classes based on OOA design:
- Server: 核心伺服器類別
- Command: 指令資料結構  
- ExecutionResult: 執行結果資料結構
- File: 檔案資料結構
"""

from .server import Server
from .command import Command
from .execution_result import ExecutionResult
from .file import File

__all__ = [
    "Server",
    "Command", 
    "ExecutionResult",
    "File"
]