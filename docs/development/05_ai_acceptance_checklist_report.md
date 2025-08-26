# User Story 驗收清單 (Acceptance Checklist)

## 目的
針對所有已實作的 User Stories 進行完整驗收，確保：
1. **Requirements 符合度** - 實作完全符合 `docs/requirements/02_user_story.md` 中的原始需求定義
2. **Test Code 純度** - 測試程式碼僅負責測試，無 production 邏輯
3. **Production Code 完整性** - 生產程式碼功能完整，無遺漏未實作項目

## 驗收方法
每個 User Story 的驗收必須：
1. **參考原始需求** - 回到 `docs/requirements/02_user_story.md` 查看該 US 的完整定義
2. **對照 BDD Feature** - 檢查 `tests/features/us{XXX}_*/` 下的 feature files 是否正確反映需求
3. **檢查實作代碼** - 確認 production code 完全實現需求，無遺漏或偏差

## 驗收狀態
- ⏳ **待驗收** - 尚未進行驗收檢查
- ✅ **驗收通過** - 所有檢查項目符合標準
- ❌ **驗收失敗** - 發現問題需要修正
- 🔄 **重新驗收** - 修正後等待重新檢查

---

## Phase A: 系統基石

### US-003: Default Session Auto Join ✅
**需求描述**: Client 自動加入預設 session，支援 session isolation
**驗收項目**:
- [x] **Requirements 符合度**
  - [x] Client 首次 polling 時自動建立或加入 default session
  - [x] 支援指定 session-id 的協作模式
  - [x] Session 之間完全隔離
  - [x] API 端點正確實作並符合規格

- [x] **Test Code 純度**
  - [x] BDD feature files 只描述行為，不包含實作邏輯
  - [x] Step implementations 只執行測試操作，不承擔 business logic
  - [x] Test fixtures 與 production code 清楚分離
  - [x] 無 test code 直接呼叫 production classes 的 private methods

- [x] **Production Code 完整性**
  - [x] SessionRepository 完整實作 session 管理邏輯
  - [x] Client polling API 完整整合 session 自動加入機制
  - [x] 無 TODO、FIXME 或 placeholder code
  - [x] 無 HTTP 501 錯誤殘留

**驗收結果**: ✅ **驗收通過**
- API `/api/sessions/default/poll` 正常運作，client 自動加入 default session
- BDD 測試通過：`test_client_automatically_joins_default_session_on_first_polling`
- Session 隔離機制正確實作於 `InMemorySessionRepository`
- Client 註冊狀態 (new/existing) 回應正確

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-003 段落
- **BDD 測試**: `tests/features/us003_default_session_auto_join/`
- **Production Code**: 
  - `public_tunnel/repositories/session_repository.py`
  - `public_tunnel/routers/client_polling.py`

---

### US-005: Client Presence Tracking ✅
**需求描述**: 追蹤 client 在線狀態，支援 online/offline 判定
**驗收項目**:
- [x] **Requirements 符合度**
  - [x] Polling 時自動更新 last_seen timestamp
  - [x] 支援可配置的超時閾值判定離線狀態
  - [x] Presence query API 正確回應 client 狀態
  - [x] 狀態判定邏輯準確可靠

- [x] **Test Code 純度**
  - [x] BDD scenarios 專注行為驗證，不涉及實作細節
  - [x] 時間相關測試使用 mock 或固定時間，避免不穩定測試
  - [x] Test setup 清楚分離，不與 production service 混淆
  - [x] 無測試程式碼直接操作 production 資料結構

- [x] **Production Code 完整性**
  - [x] ClientPresenceTracker 服務完整實作
  - [x] 整合到 polling API 的自動更新機制
  - [x] 可配置的超時設定管理
  - [x] Presence query API 端點完整實作

**驗收結果**: ✅ **驗收通過**
- API `/api/sessions/{session_id}/clients/{client_id}/presence` 正常運作
- BDD 測試通過：`test_client_presence_is_tracked_through_polling`
- `InMemoryClientPresenceTracker` 完整實作 presence 追蹤邏輯
- Client polling 時自動更新 last_seen，狀態判定正確 (online/offline)
- 與 client polling API 正確整合

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-005 段落
- **BDD 測試**: `tests/features/us005_client_presence_tracking/`
- **Production Code**: 
  - `public_tunnel/services/client_presence_tracker.py`
  - `public_tunnel/routers/client_presence_query.py`

---

### US-016: Client Offline Status Management ✅
**需求描述**: 基於 presence tracking 的離線狀態管理機制
**驗收項目**:
- [x] **Requirements 符合度**
  - [x] 基於可配置時間閾值的自動離線偵測
  - [x] 狀態自動轉換（online ↔ offline）
  - [x] 離線 client 拒絕命令提交的業務規則
  - [x] 離線閾值配置管理 API

- [x] **Test Code 純度**
  - [x] 測試使用時間 mock 確保可重複性
  - [x] BDD scenarios 描述業務行為，不暴露實作邏輯
  - [x] 測試資料設定與 production code 分離
  - [x] 無測試直接修改 production 狀態管理邏輯

- [x] **Production Code 完整性**
  - [x] 離線狀態偵測機制完整實作
  - [x] Client 狀態轉換邏輯正確
  - [x] 強制狀態檢查功能完整
  - [x] 配置管理 API 端點實作完整

**驗收結果**: ✅ **驗收通過**
- 離線閾值配置 API 正常運作：`GET /api/configuration/offline-threshold`
- 閾值更新 API 正常運作：`PUT /api/configuration/offline-threshold`
- BDD 測試通過：`test_client_is_marked_offline_after_polling_timeout`
- `OfflineStatusManager` 完整實作離線狀態管理邏輯
- Client 狀態自動轉換機制正確 (polling timeout 後自動標記 offline)
- 與 command submission 正確整合 (離線 client 拒絕指令)

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-016 段落
- **BDD 測試**: `tests/features/us016_client_offline_status_management/`
- **Production Code**: 
  - `public_tunnel/services/client_presence_tracker.py` (enhanced)
  - `public_tunnel/routers/client_offline_config.py`

---

## Phase B: 核心指令流程

### US-006: Targeted Client Command Submission ✅
**需求描述**: 向指定 client 提交指令，支援多 client session 隔離
**驗收項目**:
- [x] **Requirements 符合度**
  - [x] API 端點接受 session_id 和 client_id 參數
  - [x] 指令正確排入指定 client 的佇列
  - [x] Session 內多 client 指令分發隔離
  - [x] 錯誤處理機制完整（client 不存在等）

- [x] **Test Code 純度**
  - [x] BDD scenarios 驗證指令分發行為，不涉及佇列實作
  - [x] Test setup 模擬真實 client 行為，不直接操作內部狀態
  - [x] 多 client 測試清楚隔離，避免互相影響
  - [x] 無測試程式碼承擔指令佇列管理責任

- [x] **Production Code 完整性**
  - [x] CommandQueueManager 完整實作 FIFO 佇列管理
  - [x] API endpoint 完整實作並整合錯誤處理
  - [x] Client 隔離機制正確實作
  - [x] 依賴注入架構正確整合

**驗收結果**: ✅ **驗收通過**
- 指令提交 API 正常運作：`POST /api/sessions/{session_id}/commands/submit`
- BDD 測試通過：`test_submit_command_to_valid_target_client`
- `CommandQueueManager` 完整實作指令佇列管理（thread-safe FIFO）
- 整合 US-013 (client 不存在) 和 US-014 (client 離線) 錯誤處理
- Client 隔離機制正確：不同 client 的指令分別排隊
- 回應包含 command_id、execution_status、submission_timestamp 等完整資訊

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-006 段落
- **BDD 測試**: `tests/features/us006_targeted_client_command_submission/`
- **Production Code**: 
  - `public_tunnel/services/command_queue_manager.py`
  - `public_tunnel/routers/submit_commands_to_target_clients.py`

---

### US-007: Command FIFO Queue Management ✅
**需求描述**: 指令佇列 FIFO 管理，確保執行順序
**驗收項目**:
- [x] **Requirements 符合度**
  - [x] 嚴格的 FIFO 指令佇列實作
  - [x] Polling API 每次只返回一個指令
  - [x] 指令從佇列正確移除避免重複執行
  - [x] 多指令佇列順序正確性

- [x] **Test Code 純度**
  - [x] BDD 測試專注驗證 FIFO 行為，不涉及資料結構實作
  - [x] 測試 scenario 清楚分離不同的佇列狀態
  - [x] 無測試程式碼直接操作佇列內部結構
  - [x] 使用 API 呼叫驗證行為，不依賴實作細節

- [x] **Production Code 完整性**
  - [x] FIFO 佇列邏輯完整實作
  - [x] Client polling API 正確整合佇列管理
  - [x] 單指令返回約束正確實作
  - [x] CommandQueueManager 與現有架構整合

**驗收結果**: ✅ **驗收通過**
- FIFO 佇列 API 正常運作：`GET /api/sessions/{session_id}/clients/{client_id}/commands/poll`
- BDD 測試通過：`test_multiple_commands_queued_for_same_client_are_returned_in_fifo_order`
- FIFO 順序驗證：3個指令依序提交後，polling 依 command-1, command-2, command-3 順序返回
- 每次 polling 只返回一個指令，佇列大小資訊正確 (2→1→0)
- 使用 `collections.deque` 確保 thread-safe FIFO 實作
- 佇列空時返回 null command，queue_size 為 0

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-007 段落
- **BDD 測試**: `tests/features/us007_command_fifo_queue_management/`
- **Production Code**: 
  - `public_tunnel/services/command_queue_manager.py` (enhanced)
  - `public_tunnel/routers/client_command_polling.py`

---

### US-009: Client Single Command Retrieval ✅
**需求描述**: Client-focused 單一指令接收機制
**驗收項目**:
- [x] **Requirements 符合度**
  - [x] 每次 polling 只返回一個指令
  - [x] 指令從佇列移除避免重複
  - [x] 提供 `has_more_commands` 和 `queue_size` 資訊
  - [x] API 端點正確實作並符合規格

- [x] **Test Code 純度**
  - [x] BDD scenarios 驗證單指令行為，不涉及實作細節
  - [x] 測試從 client 角度驗證行為，不直接操作伺服器狀態
  - [x] Queue 狀態驗證透過 API 回應，不直接檢查內部狀態
  - [x] 無測試程式碼承擔佇列管理邏輯

- [x] **Production Code 完整性**
  - [x] 單指令返回邏輯完整實作
  - [x] ClientCommandRetrievalResponse 模型完整
  - [x] 佇列狀態資訊提供機制完整
  - [x] API 端點與服務層正確整合

**驗收結果**: ✅ **驗收通過**
- 單指令接收 API 正常運作：`GET /api/sessions/{session_id}/clients/{client_id}/command`
- BDD 測試通過：`test_client_receives_exactly_one_command_per_polling_request`
- API 正確回應單一指令並從佇列移除，提供 `has_more_commands` 和 `queue_size`
- `get_next_command_with_queue_info` 方法完整實作並整合到 API 端點
- Client 可透過 queue 資訊控制執行節奏

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-009 段落
- **BDD 測試**: `tests/features/us009_client_single_command_retrieval/`
- **Production Code**: 
  - `public_tunnel/models/command.py`
  - `public_tunnel/routers/client_single_command_retrieval.py`

---

### US-021: Unified Result Query Mechanism ✅
**需求描述**: 統一結果查詢機制，支援 sync 和 async 指令結果
**驗收項目**:
- [x] **Requirements 符合度**
  - [x] 統一的結果查詢 API，不分 sync/async
  - [x] command-id 索引機制正確實作
  - [x] 結果儲存和檢索機制完整
  - [x] 一致的回應格式設計

- [x] **Test Code 純度**
  - [x] BDD 測試驗證統一查詢行為，不依賴儲存實作
  - [x] 測試涵蓋各種結果類型，但不涉及內部資料結構
  - [x] 使用 command-id 驗證結果，不直接存取儲存層
  - [x] 無測試程式碼實作結果管理邏輯

- [x] **Production Code 完整性**
  - [x] ExecutionResultManager 完整實作
  - [x] UnifiedResultQueryResponse 模型完整
  - [x] 指令ID索引機制正確實作
  - [x] API 端點與現有架構整合

**驗收結果**: ✅ **驗收通過**
- 統一結果查詢 API 正常運作：`GET /api/sessions/{session_id}/results/{command_id}`
- BDD 測試通過：`test_all_command_results_are_stored_with_commandid_indexing`
- 不論快速或慢速指令都使用相同的 API 格式和端點
- `InMemoryExecutionResultManager` 完整實作 command-id 索引機制
- `UnifiedResultQueryResponse` 模型提供一致的結果格式
- API 支援結果提交和查詢的完整週期

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-021 段落
- **BDD 測試**: `tests/features/us021_unified_result_query_mechanism/`
- **Production Code**: 
  - `public_tunnel/services/execution_result_manager.py`
  - `public_tunnel/models/execution_result.py`
  - `public_tunnel/routers/unified_result_query_mechanism.py`

---

## Phase C: 錯誤處理與檔案管理

### 錯誤處理群組 (C1)

### US-013: Non Existent Client Error Handling ✅
**需求描述**: 處理不存在 client 的錯誤情況
**驗收項目**:
- [x] **Requirements 符合度**
  - [x] 正確偵測不存在的 client
  - [x] 404 錯誤回應格式正確
  - [x] 錯誤訊息清楚明確
  - [x] 不影響正常 client 的操作

- [x] **Test Code 純度**
  - [x] BDD scenarios 專注錯誤行為驗證
  - [x] 測試不直接修改 client 註冊狀態
  - [x] 使用 API 呼叫測試錯誤處理
  - [x] 無測試程式碼實作錯誤檢查邏輯

- [x] **Production Code 完整性**
  - [x] NonExistentClientErrorResponse 模型完整
  - [x] Client 存在性檢查邏輯完整
  - [x] 錯誤回應機制正確實作
  - [x] 向後相容性確保

**驗收結果**: ✅ **驗收通過**
- 不存在 client 錯誤處理正常運作：404 狀態碼，清晰錯誤訊息
- BDD 測試通過：`test_reject_command_targeting_nonexistent_client`
- 透過 `ClientPresenceTracker` 檢查 client 是否曾經註冊
- 錯誤訊息包含具體 client ID 和註冊要求說明
- 指令不會被排入不存在 client 的佇列中
- 整合在指令提交流程中，不影響正常 client 操作

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-013 段落
- **BDD 測試**: `tests/features/us013_non_existent_client_error_handling/`
- **Production Code**: 
  - `public_tunnel/models/command.py` (NonExistentClientErrorResponse)
  - `public_tunnel/routers/submit_commands_to_target_clients.py` (enhanced)

---

### US-014: Offline Client Command Rejection ✅
**需求描述**: 拒絕向離線 client 提交指令
**驗收項目**:
- [x] **Requirements 符合度**
  - [x] 正確整合離線狀態檢查
  - [x] 422 錯誤回應當 client 離線
  - [x] 離線檢查邏輯準確
  - [x] 只向線上 client 提交指令

- [x] **Test Code 純度**
  - [x] BDD 測試驗證離線拒絕行為
  - [x] 測試使用時間 mock 控制離線狀態
  - [x] 無測試程式碼直接設定 client 狀態
  - [x] 透過 API 行為驗證離線檢查

- [x] **Production Code 完整性**
  - [x] 離線狀態檢查整合完整
  - [x] 422 錯誤回應機制實作
  - [x] 與 presence tracking 正確整合
  - [x] 指令提交邏輯更新完整

**驗收結果**: ✅ **驗收通過**
- 離線 client 指令拒絕機制正常運作：422 狀態碼，防止指令遺失
- BDD 測試通過：`test_reject_command_targeting_offline_client`
- `OfflineStatusManager.is_client_eligible_for_commands` 正確判定 client 資格
- 錯誤訊息清楚說明離線狀態和指令防遺失原因
- 指令不會被排入離線 client 的佇列中
- 與 US-013 (不存在 client) 錯誤處理協同運作

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-014 段落
- **BDD 測試**: `tests/features/us014_offline_client_command_rejection/`
- **Production Code**: 
  - `public_tunnel/services/offline_status_manager.py`
  - `public_tunnel/routers/submit_commands_to_target_clients.py` (enhanced)

---

### US-015: Client Execution Error Reporting ⏳
**需求描述**: Client 執行錯誤回報機制
**驗收項目**:
- [ ] **Requirements 符合度**
  - [ ] 錯誤回報 API 端點完整實作
  - [ ] 錯誤結果格式與成功結果一致
  - [ ] 統一錯誤結果查詢機制
  - [ ] AI 可一致處理成功與錯誤結果

- [ ] **Test Code 純度**
  - [ ] BDD 測試驗證錯誤回報流程
  - [ ] 測試不實作錯誤處理邏輯
  - [ ] 使用 API 驗證錯誤結果格式
  - [ ] 無測試程式碼承擔結果管理責任

- [ ] **Production Code 完整性**
  - [ ] 錯誤回報 API 端點完整實作
  - [ ] 統一結果查詢整合完整
  - [ ] 錯誤結果索引機制實作
  - [ ] 與現有結果管理系統整合

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-015 段落
- **BDD 測試**: `tests/features/us015_client_execution_error_reporting/`
- **Production Code**: 
  - `public_tunnel/routers/client_error_reporting.py`
  - `public_tunnel/services/execution_result_manager.py` (enhanced)

---

### 檔案管理群組 (C2)

### US-010: AI File Upload Feature ⏳
**需求描述**: AI 上傳檔案到 session 供 client 使用
**驗收項目**:
- [ ] **Requirements 符合度**
  - [ ] 檔案上傳 API 完整實作
  - [ ] 檔案下載 API 完整實作
  - [ ] 檔案列表 API 完整實作
  - [ ] Base64 編碼處理正確
  - [ ] Session-based 檔案隔離

- [ ] **Test Code 純度**
  - [ ] BDD 測試驗證檔案操作行為
  - [ ] 測試使用標準檔案格式，不涉及儲存實作
  - [ ] 檔案內容驗證透過 API，不直接存取檔案系統
  - [ ] 無測試程式碼實作檔案管理邏輯

- [ ] **Production Code 完整性**
  - [ ] FileManager 服務完整實作
  - [ ] InMemoryFileManager 實作完整
  - [ ] 檔案資料模型架構完整
  - [ ] 依賴注入與路由整合

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-010 段落
- **BDD 測試**: `tests/features/us010_ai_file_upload_feature/`
- **Production Code**: 
  - `public_tunnel/services/file_manager.py`
  - `public_tunnel/routers/ai_file_upload.py`

---

### US-012: Session File Access Isolation ⏳
**需求描述**: Session 間檔案存取隔離機制
**驗收項目**:
- [ ] **Requirements 符合度**
  - [ ] 檔案存取權限驗證完整
  - [ ] 跨 session 存取正確拒絕
  - [ ] 存取違規記錄機制
  - [ ] 安全檔案下載功能

- [ ] **Test Code 純度**
  - [ ] BDD 測試驗證存取隔離行為
  - [ ] 測試不直接操作檔案權限設定
  - [ ] 透過不同 session 驗證隔離效果
  - [ ] 無測試程式碼實作權限檢查邏輯

- [ ] **Production Code 完整性**
  - [ ] SessionFileAccessValidator 完整實作
  - [ ] 檔案存取驗證 API 完整
  - [ ] 存取違規記錄機制實作
  - [ ] 與現有檔案管理整合

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-012 段落
- **BDD 測試**: `tests/features/us012_session_file_access_isolation/`
- **Production Code**: 
  - `public_tunnel/services/session_file_access_validator.py`
  - `public_tunnel/routers/file_access_validation.py`

---

### US-011: Client Result File Upload ⏳
**需求描述**: Client 上傳執行結果檔案機制
**驗收項目**:
- [ ] **Requirements 符合度**
  - [ ] Client 結果檔案上傳 API 完整
  - [ ] 檔案 metadata 管理完整
  - [ ] file-id 生成和索引機制
  - [ ] 與指令結果系統整合

- [ ] **Test Code 純度**
  - [ ] BDD 測試驗證檔案上傳流程
  - [ ] 測試不實作檔案處理邏輯
  - [ ] 使用 API 驗證 metadata 和索引
  - [ ] 無測試程式碼承擔檔案管理責任

- [ ] **Production Code 完整性**
  - [ ] Client 檔案上傳 API 實作完整
  - [ ] File metadata 管理機制完整
  - [ ] 與結果查詢系統整合
  - [ ] file-id 索引機制實作

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-011 段落
- **BDD 測試**: `tests/features/us011_client_result_file_upload/`
- **Production Code**: 
  - `public_tunnel/routers/client_file_upload.py`
  - `public_tunnel/models/file_metadata.py`

---

### US-022: File Unique Identification ⏳
**需求描述**: 檔案唯一識別機制，處理重名檔案
**驗收項目**:
- [ ] **Requirements 符合度**
  - [ ] 檔案唯一 ID 生成機制
  - [ ] 重名檔案區分機制
  - [ ] 跨 session 檔案識別
  - [ ] 檔案 metadata 支援識別

- [ ] **Test Code 純度**
  - [ ] BDD 測試驗證檔案識別行為
  - [ ] 測試不實作 ID 生成邏輯
  - [ ] 透過 metadata 驗證檔案區分
  - [ ] 無測試程式碼承擔識別機制責任

- [ ] **Production Code 完整性**
  - [ ] 檔案 ID 生成機制完整
  - [ ] 重名處理邏輯實作
  - [ ] Metadata 支援識別資訊
  - [ ] 與檔案管理系統整合

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-022 段落
- **BDD 測試**: `tests/features/us022_file_unique_identification/`
- **Production Code**: 
  - `public_tunnel/services/file_manager.py` (enhanced)
  - `public_tunnel/models/file_metadata.py` (enhanced)

---

## Phase D: 進階功能

### US-004: Specified Session Collaboration Mode ⏳
**需求描述**: 指定 session 的協作模式
**驗收項目**:
- [ ] **Requirements 符合度**
  - [ ] Client 可指定加入特定 session
  - [ ] 多 client 協作功能正常
  - [ ] Session 存在性檢查機制
  - [ ] 協作模式下的隔離保證

- [ ] **Test Code 純度**
  - [ ] BDD 測試驗證協作行為
  - [ ] 測試不實作 session 管理邏輯
  - [ ] 多 client 測試清楚隔離
  - [ ] 無測試程式碼承擔協作管理責任

- [ ] **Production Code 完整性**
  - [ ] Session 指定機制完整實作
  - [ ] 多 client 協作邏輯完整
  - [ ] Session 檢查機制實作
  - [ ] 與現有 session 系統整合

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-004 段落
- **BDD 測試**: `tests/features/us004_specified_session_collaboration_mode/`
- **Production Code**: 
  - `public_tunnel/repositories/session_repository.py` (enhanced)
  - `public_tunnel/routers/client_polling.py` (enhanced)

---

### US-008: Auto Async Response with Initial Wait ⏳
**需求描述**: 自動異步回應機制，支援初始等待
**驗收項目**:
- [ ] **Requirements 符合度**
  - [ ] 快速指令同步回應機制
  - [ ] 慢速指令自動轉異步機制
  - [ ] 可配置的等待閾值
  - [ ] 統一的結果查詢介面

- [ ] **Test Code 純度**
  - [ ] BDD 測試驗證同步/異步轉換行為
  - [ ] 測試使用時間 mock 控制執行時間
  - [ ] 不實作指令執行邏輯
  - [ ] 透過 API 驗證轉換行為

- [ ] **Production Code 完整性**
  - [ ] 異步轉換邏輯完整實作
  - [ ] 等待閾值配置機制
  - [ ] 與統一結果查詢整合
  - [ ] 指令執行狀態管理

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-008 段落
- **BDD 測試**: `tests/features/us008_auto_async_response_with_initial_wait/`
- **Production Code**: 
  - `public_tunnel/services/async_command_manager.py`
  - `public_tunnel/routers/command_submission.py` (enhanced)

---

## Phase E: 監控與管理

### US-018: Command Execution Status Query ⏳
**需求描述**: 指令執行狀態查詢機制
**驗收項目**:
- [ ] **Requirements 符合度**
  - [ ] 指令狀態查詢 API 完整實作
  - [ ] 支援 pending, running, completed 狀態
  - [ ] 不存在指令的錯誤處理
  - [ ] 狀態更新機制正確

- [ ] **Test Code 純度**
  - [ ] BDD 測試驗證狀態查詢行為
  - [ ] 測試不實作狀態管理邏輯
  - [ ] 透過 API 驗證狀態轉換
  - [ ] 無測試程式碼承擔狀態更新責任

- [ ] **Production Code 完整性**
  - [ ] 指令狀態管理機制完整
  - [ ] 狀態查詢 API 實作完整
  - [ ] 狀態轉換邏輯正確
  - [ ] 錯誤處理機制實作

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-018 段落
- **BDD 測試**: `tests/features/us018_command_execution_status_query/`
- **Production Code**: 
  - `public_tunnel/services/execution_result_manager.py` (enhanced)
  - `public_tunnel/routers/command_status_query.py`

---

### US-019: Session Command History Query ⏳
**需求描述**: Session 指令歷史查詢功能
**驗收項目**:
- [ ] **Requirements 符合度**
  - [ ] Session 指令歷史查詢 API
  - [ ] 指令 ID 列表回應正確
  - [ ] 與指令詳細查詢整合
  - [ ] 空 session 處理正確

- [ ] **Test Code 純度**
  - [ ] BDD 測試驗證歷史查詢行為
  - [ ] 測試不實作歷史管理邏輯
  - [ ] 透過 API 驗證歷史記錄
  - [ ] 無測試程式碼承擔歷史儲存責任

- [ ] **Production Code 完整性**
  - [ ] 指令歷史管理機制完整
  - [ ] 歷史查詢 API 實作完整
  - [ ] 與結果查詢系統整合
  - [ ] Session 隔離機制正確

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-019 段落
- **BDD 測試**: `tests/features/us019_session_command_history_query/`
- **Production Code**: 
  - `public_tunnel/services/execution_result_manager.py` (enhanced)
  - `public_tunnel/routers/session_command_history_query.py`

---

### US-001: Admin Session List Query ⏳
**需求描述**: Admin 查詢所有 session 列表功能
**驗收項目**:
- [ ] **Requirements 符合度**
  - [ ] Admin token 驗證機制正確
  - [ ] Session 列表查詢 API 完整
  - [ ] Admin 權限隔離機制
  - [ ] 403 錯誤處理正確

- [ ] **Test Code 純度**
  - [ ] BDD 測試驗證 admin 查詢行為
  - [ ] 測試不實作權限檢查邏輯
  - [ ] 透過 token 驗證權限機制
  - [ ] 無測試程式碼承擔權限管理責任

- [ ] **Production Code 完整性**
  - [ ] AdminTokenValidator 完整實作
  - [ ] Session 列表查詢 API 實作
  - [ ] Admin 權限檢查機制
  - [ ] 與 session repository 整合

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-001 段落
- **BDD 測試**: `tests/features/us001_admin_session_list_query/`
- **Production Code**: 
  - `public_tunnel/services/admin_token_validator.py`
  - `public_tunnel/routers/list_all_sessions_for_admin.py`

---

### US-002: Regular User Access Restriction ⏳
**需求描述**: 一般使用者存取限制機制
**驗收項目**:
- [ ] **Requirements 符合度**
  - [ ] 無效 admin token 拒絕存取
  - [ ] 缺少 admin token 拒絕存取
  - [ ] 403 錯誤回應正確
  - [ ] 不影響正常 admin 操作

- [ ] **Test Code 純度**
  - [ ] BDD 測試驗證存取限制行為
  - [ ] 測試不實作權限驗證邏輯
  - [ ] 透過不同 token 驗證限制機制
  - [ ] 無測試程式碼承擔存取控制責任

- [ ] **Production Code 完整性**
  - [ ] 存取限制機制整合完整
  - [ ] 使用現有 AdminTokenValidator
  - [ ] 403 錯誤回應實作正確
  - [ ] 與現有權限系統整合

**驗收參考資料**:
- **需求定義**: `docs/requirements/02_user_story.md` → US-002 段落
- **BDD 測試**: `tests/features/us002_regular_user_access_restriction/`
- **Production Code**: 
  - `public_tunnel/services/admin_token_validator.py` (reused)

---

## 驗收執行指南

### 執行方式
1. **個別 User Story 驗收**: 逐一檢查每個 User Story 的三個驗收項目
2. **階段性批量驗收**: 按 Phase A-E 進行批量驗收
3. **完整專案驗收**: 所有 User Story 一次性驗收

### 檢查工具與步驟
1. **Requirements 符合度檢查**:
   - 開啟 `docs/requirements/02_user_story.md` 找到對應 US 定義
   - 對照 BDD feature files 確保需求正確轉換為測試場景
   - 檢查 API 端點、參數、回應格式是否符合需求規格
   
2. **Test Code 純度審查**:
   - 檢查 BDD feature files 只描述行為，不涉及實作細節
   - 確認 step implementations 只執行測試操作，不承擔業務邏輯
   - 驗證測試與 production code 職責分離清楚
   
3. **Production Code 完整性驗證**:
   - 程式碼審查確認所有需求功能都有實作
   - 檢查無 TODO、FIXME、HTTP 501 等未完成標記
   - 執行功能測試驗證實作正確性

### 驗收標準
- **通過標準**: 所有檢查項目都必須符合要求
- **失敗處理**: 發現問題立即記錄，修正後重新驗收
- **品質保證**: 確保每個 User Story 都達到生產就緒品質

### 文件維護
- 每次驗收後更新此文件的驗收狀態
- 記錄發現的問題和修正措施
- 保持驗收記錄的完整性和可追蹤性

---

## 最後更新
- **建立日期**: 2025-08-25
- **更新日期**: 2025-08-26
- **總 User Stories**: 21 個 (US-017 deprecated)
- **驗收狀態**: Phase A-B-C 部分驗收完成 ✅
  - **已驗收**: 9 個 (US-003, US-005, US-016, US-006, US-007, US-009, US-021, US-013, US-014) 
  - **待驗收**: 12 個 (其餘 Phase B-E User Stories)
- **下一步**: 繼續執行 Phase B-E 的其他 User Story 驗收

## 驗收總結 (Phase A)

### 已驗收通過的 User Stories:

#### Phase A: 系統基石
1. **US-003: Default Session Auto Join** ✅
   - Client 自動加入預設 session 機制完全正常
   - Session 隔離和協作模式支援完整

2. **US-005: Client Presence Tracking** ✅
   - Presence tracking 整合到 polling API 正常運作
   - Online/offline 狀態判定邏輯正確實作

3. **US-016: Client Offline Status Management** ✅
   - 離線閾值配置和管理 API 正常運作
   - 離線 client 拒絕指令機制正確整合

#### Phase B: 核心指令流程
4. **US-006: Targeted Client Command Submission** ✅
   - 指令提交到特定 client 功能正常
   - 錯誤處理機制完整 (client 不存在/離線)

5. **US-007: Command FIFO Queue Management** ✅
   - FIFO 佇列管理完全正確
   - 每次 polling 只返回一個指令，順序保證

6. **US-009: Client Single Command Retrieval** ✅
   - Client-focused 單指令接收 API 正常運作
   - 提供執行節奏控制機制 (has_more_commands, queue_size)

7. **US-021: Unified Result Query Mechanism** ✅
   - 統一結果查詢 API 支援不同執行時間的指令
   - Command-id 索引機制和一致性結果格式完整實作

#### Phase C: 錯誤處理與檔案管理
8. **US-013: Non Existent Client Error Handling** ✅
   - 不存在 client 錯誤處理機制完整實作
   - 404 錯誤回應和清晰錯誤訊息，指令不會被誤加入佇列

9. **US-014: Offline Client Command Rejection** ✅
   - 離線 client 指令拒絕機制完整實作
   - 422 錯誤回應和指令防遺失保護機制

### 驗收品質保證:
- 所有 BDD 測試均通過
- API 端點功能驗證正常
- Production code 無 TODO/FIXME 殘留
- Test code 與 production code 職責分離清楚
- Requirements 符合度、Test Code 純度、Production Code 完整性三大驗收項目全數符合標準