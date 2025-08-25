# public-tunnel User Stories 文件

## 互動路徑總覽

```
AI助手
├── 發現可用資源
│   ├── 查詢所有sessions (需admin token)
│   │   └── Server回應
│   │       ├── 選擇特定session → 查詢該session的clients
│   │       └── 跨session操作 → 對不同session下指令
│   └── 查詢session內clients (一般權限)
│       └── Server回應client清單
│           ├── 選擇線上client → 執行指令流程
│           ├── 發現離線client → 等待或選擇其他client
│           └── 無可用client → 等待client上線
│
├── 執行指令操作
│   ├── 送出同步指令
│   │   └── Server接收並分發
│   │       └── Client polling取得
│   │           └── Client執行
│   │               ├── 成功執行 → Client回報結果 → Server儲存 → AI助手直接取得結果
│   │               └── 執行失敗 → Client回報錯誤 → Server儲存 → AI助手取得錯誤訊息
│   ├── 送出非同步指令
│   │   └── Server接收並分發
│   │       ├── 立即回應command-id → AI助手polling查詢結果
│   │       └── Client polling取得
│   │           └── Client執行
│   │               ├── 成功執行 → Client回報結果 → AI助手查詢取得
│   │               └── 執行失敗 → Client回報錯誤 → AI助手查詢取得
│   └── 送出同步指令但執行時間過長
│       └── Server自動轉非同步
│           └── 回應command-id → AI助手改用polling查詢
│
├── 檔案操作
│   ├── 上傳檔案供client使用
│   │   └── Server儲存在session
│   │       └── 透過指令通知client → Client下載使用
│   ├── 查詢session檔案清單
│   │   └── Server回應檔案列表
│   │       ├── 選擇下載特定檔案 → Server提供檔案內容
│   │       └── 查看檔案摘要 → 決定是否下載
│   └── 查詢指令結果中的檔案
│       └── Server回應檔案參考
│           └── 根據file-id下載需要的檔案
│
└── 查詢操作歷史
    ├── 查詢session內的command-id清單
    │   └── Server回應指令列表
    │       └── 選擇特定command-id → 查詢詳細結果
    └── 查詢特定command-id的結果
        └── Server回應
            ├── 結果已完成 → 取得完整結果
            ├── 結果執行中 → 繼續polling等待
            └── 結果執行失敗 → 取得錯誤訊息

Client端
├── 啟動連線
│   ├── 使用預設參數 (hostname + 隨機session)
│   │   └── Server建立獨立session
│   │       └── 開始polling循環
│   ├── 指定client-id但使用預設session
│   │   └── Server記錄client-id
│   │       └── 加入default session
│   └── 指定client-id和session-id
│       └── Server檢查session存在性
│           ├── session存在 → 加入現有session (協作模式)
│           └── session不存在 → 建立新session
│
├── Polling循環
│   ├── 定時發送polling請求
│   │   └── Server檢查command queue
│   │       ├── 有待執行指令 → 回傳一個指令 → Client取得並執行
│   │       └── 無待執行指令 → 回傳空結果 → Client繼續等待
│   ├── 更新存在證明
│   │   └── Server記錄最後polling時間
│   │       ├── 保持線上狀態 → 可接收新指令
│   │       └── 超過30秒無polling → 標記離線狀態
│   └── 網路斷線重連
│       └── 持續嘗試polling → 網路恢復後自動重新上線
│
├── 指令執行
│   ├── 接收到指令
│   │   └── 從command queue取出
│   │       ├── 指令被移除 → 開始執行 → 產生結果
│   │       └── 繼續polling等待下一個指令
│   ├── 執行成功
│   │   └── 產生結果內容
│   │       ├── 簡單結果 → 直接回報內容
│   │       └── 複雜結果 → 上傳檔案 + 回報檔案參考
│   └── 執行失敗
│       └── 產生錯誤訊息 → 回報錯誤結果
│
└── 檔案操作
    ├── 下載AI助手提供的檔案
    │   └── Server提供檔案內容
    ├── 上傳執行結果檔案
    │   └── Server儲存在session
    │       └── 生成file-id和metadata
    └── 處理指令相關的檔案操作
        ├── 讀取檔案 → 上傳內容
        └── 修改檔案 → 上傳新版本

Server端 (被動響應)
├── 接收AI助手請求
│   ├── session列表查詢 (需admin token)
│   │   ├── 驗證token → 有效token → 回傳所有sessions
│   │   └── 驗證失敗 → 回傳403錯誤
│   ├── session內client查詢
│   │   └── 回傳client列表和狀態
│   ├── 指令提交
│   │   ├── 檢查target_client → 放入對應command queue
│   │   └── 根據模式回應 (同步等待/非同步回傳command-id)
│   ├── 結果查詢
│   │   └── 從result queue取得結果
│   └── 檔案操作請求
│       ├── 檔案上傳 → 儲存在session
│       ├── 檔案下載 → 提供檔案內容
│       └── 檔案清單 → 回傳session內檔案列表
│
├── 接收Client polling
│   ├── 記錄存在證明
│   │   └── 更新最後polling時間
│   ├── 檢查command queue
│   │   ├── 有指令 → 回傳一個指令並從queue移除
│   │   └── 無指令 → 回傳空結果
│   └── 接收執行結果
│       └── 儲存到result queue (以command-id為索引)
│
└── 狀態管理
    ├── 監控client狀態
    │   ├── 定期檢查最後polling時間
    │   └── 超過閾值 → 標記為離線
    ├── 維護各種queue
    │   ├── command queue (每個client一個)
    │   ├── result queue (以command-id索引)
    │   └── file storage (以session隔離)
    └── Session管理
        ├── 自動建立新session
        ├── 管理session內的資源
        └── 長期保留歷史資料
```

## 概述

### 專案背景
public-tunnel 是一個為 AI 助手設計的網路隧道解決方案，讓 AI 能夠控制位於無法直接存取網路環境中的裝置。系統採用被動式設計，透過 HTTP polling 機制實作通訊。

### User Stories 範圍與目標
本文件定義了 public-tunnel 系統的核心業務規則，每個 User Story 代表一個可測試的功能單元。這些 User Stories 將作為：
- API 設計的需求依據
- 測試案例的設計基礎
- 系統行為的明確規範

### 角色定義
- **AI 助手**：透過 HTTP API 送出指令並查詢結果的外部系統
- **Client 端**：執行指令的目標裝置，透過 polling 機制與 server 通訊
- **Server 端**：被動響應的中介系統，負責指令分發和結果管理

### 從互動路徑萃取 User Stories
上述樹狀結構展示了所有可能的系統互動流程。我們從中萃取出核心的業務規則，每個規則對應一個 User Story。這些 User Stories 遵循 BRIEF 原則：Business rule focused、Repeatable、Independent、Estimable、Fine-grained。

## 核心 User Stories

### 權限控制

**US-001**: Admin Session List Query
```
As an admin user
I want to list all sessions with valid token
So that I can manage the entire system

Acceptance Criteria:
- Given I have a valid admin token
- When I query GET /api/sessions
- Then I should receive a list of all sessions
- And each session should include basic metadata
```

**US-002**: Regular User Access Restriction
```
As a regular user
I want to be denied when trying to list all sessions
So that system security is maintained

Acceptance Criteria:
- Given I don't have a valid admin token
- When I query GET /api/sessions
- Then I should receive a 403 Forbidden response
- And I should not see any session information
```

### Session 管理

**US-003**: Default Session Auto Join
```
As a client
I want to automatically join default session when no session-id specified
So that I can start working without manual configuration

Acceptance Criteria:
- Given I start polling without specifying session-id
- When I send my first polling request
- Then I should be automatically assigned to default session
- And my client-id should be recorded in the session
```

**US-004**: Specified Session Collaboration Mode
```
As a client
I want to join existing session when session-id is specified
So that I can collaborate with other clients

Acceptance Criteria:
- Given there is an existing session with specified session-id
- When I start polling with that session-id
- Then I should join the existing session
- And I should be able to see other clients in the same session
```

**US-005**: Client Presence Tracking
```
As a server
I want to track client presence through polling
So that I can maintain accurate client status

Acceptance Criteria:
- Given a client is polling regularly
- When the client sends polling requests
- Then I should update the client's last_seen timestamp
- And the client should be marked as online
```

**US-016**: Client Offline Status Management
```
As a server
I want to mark clients offline after configured threshold of no polling
So that system state reflects reality

Acceptance Criteria:
- Given a client has stopped polling
- When the configured time threshold has passed since last_seen
- Then the client should be marked as offline
- And the client should not receive new commands
```

### 指令執行

**US-006**: Targeted Client Command Submission
```
As an AI assistant
I want to submit commands to specific clients
So that tasks are executed on target machines

Acceptance Criteria:
- Given I have a valid target client-id
- When I submit a command with target_client specified
- Then the command should be queued for that specific client
- And only that client should receive the command
```

**US-007**: Command FIFO Queue Management
```
As a server
I want to queue commands in FIFO order
So that commands are processed fairly

Acceptance Criteria:
- Given multiple commands are submitted to the same client
- When the client polls for commands
- Then commands should be returned in first-in-first-out order
- And each polling should return only one command
```

**US-008**: Auto Async Response with Initial Wait
```
As a server
I want to wait briefly for command completion before switching to async response
So that fast commands return immediately while slow commands use polling

Acceptance Criteria:
- Given a command is submitted
- When execution completes within the configured threshold
- Then the result should be returned immediately
- When execution exceeds the threshold
- Then a command-id should be returned for polling
```

**US-009**: Client Single Command Retrieval
```
As a client
I want to receive one command at a time when polling
So that I can control my execution pace

Acceptance Criteria:
- Given there are multiple commands in my queue
- When I send a polling request
- Then I should receive exactly one command
- And that command should be removed from the queue
```

**US-020**: ~~Sync Async Mode Selection~~ (廢棄)
```
此 User Story 已廢棄，因為系統不再支援主動選擇同步或非同步模式。
所有指令均採用自動轉換機制（參見 US-008）。
```

**US-021**: Unified Result Query Mechanism
```
As a server
I want to handle all commands through the same result mechanism
So that result management is consistent

Acceptance Criteria:
- Given commands are submitted (with automatic timeout handling)
- When results are generated
- Then all results should be stored with command-id indexing
- And results should be queryable through the same API regardless of execution time
```

### 錯誤處理

**US-013**: Non Existent Client Error Handling
```
As a server
I want to reject commands targeting non-existent clients
So that errors are handled gracefully

Acceptance Criteria:
- Given a command targets a non-existent client-id
- When the command is submitted
- Then I should return an appropriate error response
- And the command should not be queued
```

**US-014**: Offline Client Command Rejection
```
As a server
I want to reject commands targeting offline clients
So that commands don't get lost

Acceptance Criteria:
- Given a client is marked as offline
- When a command targets that client
- Then I should return an error indicating client is offline
- And the command should not be queued
```

**US-015**: Client Execution Error Reporting
```
As a client
I want to report execution failures in the same format as success
So that AI can handle errors consistently

Acceptance Criteria:
- Given a command execution fails
- When I report the result
- Then the error should be formatted like a normal result
- And the AI should be able to query the error like any result
```

### 檔案管理

**US-010**: AI File Upload Feature
```
As an AI assistant
I want to upload files to session
So that clients can access shared resources

Acceptance Criteria:
- Given I have a file to share
- When I upload the file to a session
- Then the file should be stored with unique file-id
- And clients in the session should be able to download it
```

**US-011**: Client Result File Upload
```
As a client
I want to upload result files with metadata
So that AI can identify and download relevant files

Acceptance Criteria:
- Given I have execution results to share
- When I upload files as part of result reporting
- Then each file should have file-id, filename, and summary
- And the AI should be able to browse and download selectively
```

**US-012**: Session File Access Isolation
```
As a user
I want file access restricted to my session
So that data privacy is maintained

Acceptance Criteria:
- Given files are uploaded to a session
- When users try to access files
- Then only users within the same session should have access
- And cross-session file access should be denied
```

**US-022**: File Unique Identification
```
As an AI assistant
I want files identified by unique file-id
So that I can handle duplicate filenames correctly

Acceptance Criteria:
- Given multiple files with the same name exist
- When I query or download files
- Then each file should have a unique file-id
- And I should be able to distinguish files by their metadata
```

### 結果查詢

**US-018**: Command Execution Status Query
```
As an AI assistant
I want to query command execution status
So that I can track progress of long-running tasks

Acceptance Criteria:
- Given I have submitted a command
- When I query the command status using command-id
- Then I should receive current execution status
- And I should know if the command is pending, running, or completed
```

**US-019**: Session Command History Query
```
As an AI assistant
I want to list command history in a session
So that I can review past operations

Acceptance Criteria:
- Given commands have been executed in a session
- When I query the command history
- Then I should receive a list of command-ids
- And I should be able to query details for each command
```

## 測試策略說明

### 測試設計原則
每個 User Story 對應一個或多個測試案例，遵循 AAA (Arrange-Act-Assert) 模式：

- **Arrange**: 使用 HTTP API 設置測試環境（模擬 AI 助手和 Client 行為）
- **Act**: 觸發被測試的 Server 端行為
- **Assert**: 驗證 Server 端的回應和狀態變化

### API 測試對應關係
每個 User Story 直接對應到具體的 API 端點測試：

**權限控制測試**:
- `GET /api/sessions` (with/without admin token)

**Session 管理測試**:
- `GET /api/session/{session-id}/poll` (client registration)
- `GET /api/session/{session-id}/clients` (client status)

**指令執行測試**:
- `POST /api/session/{session-id}/command` (command submission)
- `GET /api/session/{session-id}/poll` (command retrieval)
- `POST /api/session/{session-id}/result` (result submission)

**檔案管理測試**:
- `POST /api/session/{session-id}/files` (file upload)
- `GET /api/session/{session-id}/files` (file listing)
- `GET /api/session/{session-id}/files/{file-id}` (file download)

### 測試案例生成策略
1. **Happy Path**: 每個 User Story 的正常流程
2. **Edge Cases**: 邊界條件和異常情況
3. **Integration**: 多個 User Story 的組合情境
4. **Performance**: 大量併發和長時間執行的情境

這些 User Stories 為 public-tunnel 系統提供了完整的行為規範，確保所有核心功能都有明確的定義和測試覆蓋。