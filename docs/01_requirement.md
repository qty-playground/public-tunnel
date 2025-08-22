# public-tunnel 功能需求文件

## 專案概述

public-tunnel 是一個為 AI 助手設計的網路隧道解決方案，讓 AI 能夠控制位於無法直接存取網路環境中的裝置。

## 核心問題

需要讓 AI 助手操控其他裝置，但這些裝置通常在無法直接存取的網路上（內網、NAT 後面等環境）。

## 解決方案

裝置內部主動發起對 public-tunnel 的通訊，建立連線後等待來自 AI 助手的呼叫。

## 系統角色與職責

### AI 助手

**指令送出**
- 透過 HTTP API 提交指令到 server
- 每個指令包含指令內容和隨機 UUID (command-id)
- 可選擇同步或非同步執行模式

**執行模式選擇**
- **同步模式**：適用於快速執行的指令，server 內部等待完成後直接回應結果
- **非同步模式**：適用於長時間執行的指令，立即回應 command-id 供後續查詢
- **自動模式切換**：同步模式超過設定門檻時自動轉為非同步，僅回應 command-id

**結果查詢**
- 無論採用哪種模式，都透過相同的公開 API 使用 command-id 取得結果
- 非同步模式下持續 polling 直到取得完整結果
- 可查詢 session 內的 command-id 清單，追蹤所有已送出的指令

**檔案處理**
- 查看指令執行結果中包含的檔案清單和摘要
- 瀏覽同一個 session 下的所有檔案清單
- 根據 file-id 選擇性下載需要的檔案（需自行處理同名檔案的識別）
- 上傳檔案供 client 端使用
- 所有檔案操作限制在當前 session 範圍內

### Client 端

**基本需求**
- 能夠發起 HTTP 請求的執行環境
- 支援定時執行和迴圈的程式語言或腳本
- 具備指令執行能力（依據目標環境而定）
- 支援檔案讀寫操作

**通訊機制**
- 透過 HTTP 定時 polling 向 public-tunnel server 查詢指令
- Polling 頻率：每秒一次（可調整為更長間隔）
- 每次 polling 作為存在證明，無需額外的註冊流程
- 適合臨時、拋棄型的工作模式

**Polling 參數**
- **client-id**：預設使用 computer name 或 hostname，可透過 query string 指定
- **session-id**：預設隨機生成，可透過 query string 指定
- 兩個參數都支援自動生成或手動指定
- 多個 client 指定相同 session-id 時自動加入同一個 session（協作模式）

**指令執行**
- 接收並執行目標環境支援的指令格式
- 指令類型和語法取決於 Client 端的實作環境
- 執行結果透過統一的回報機制回傳

**結果回報**
- 使用相同的 command-id 回報執行結果
- 支援成功和錯誤兩種結果類型
- 錯誤情況（語法錯誤、資源不足、權限不足等）同樣透過結果回報機制處理
- 支援兩種結果格式：
  - **直接內容**：簡單結果直接包含在回應中
  - **檔案參考**：複雜結果上傳為檔案，提供結構化檔案資訊
- 網路斷線重連透過持續 polling 機制自動處理

**檔案管理**
- 上傳執行結果相關的檔案
- 下載 AI 助手提供的檔案
- 檔案都與特定 session 關聯

### Server 端

**設計理念**
- 採用完全被動的架構設計，不主動發起任何操作
- 等待 client 端 polling 來接收指令
- 等待 client 執行完成後主動回報結果
- 回應 AI 助手的指令送出和結果查詢請求

**Session 管理**
- 為每個 client 連線建立獨立的 session
- 支援多個 client 共用同一個 session（協作模式）
- Session 資料（檔案、指令記錄）長期保留，支援歷史查詢
- Client 狀態追蹤：最後 polling 時間超過 30 秒視為離線（可調整）
- 離線狀態的 client 會被禁止接收新指令
- **權限控制**：嚴格禁止一般使用者列舉 session 清單，僅限管理者權限（如有實作）

**指令分發**
- 接收來自 AI 助手的指令請求
- 根據執行模式提供不同的回應策略
- 將指令暫存並等待對應的 client polling
- 不提供廣播模式，AI 助手需針對特定 client 直接下指令
- 重複執行的避免依賴 AI 助手的智慧判斷

**結果管理**
- 收集來自 client 的執行結果
- 提供統一的結果查詢 API
- 管理指令執行狀態追蹤

**檔案儲存**
- 管理 session 內的檔案上傳/下載
- 檔案大小無限制
- 以 file-id 作為檔案的唯一識別，允許同名檔案存在
- 檔案存取權限嚴格限制在同一個 session 內
- 維護檔案的 metadata 和存取權限

## 技術細節

### 檔案參考格式
每個檔案包含：
- **file-id**：檔案的唯一識別碼
- **filename**：實際檔案名稱  
- **summary**：檔案內容摘要，供 AI 助手判斷是否需要下載

### Session 檔案結構
```
session{id}/
├── command_results/           # 指令執行結果
├── uploaded_files/           # client 上傳的檔案
├── shared_files/            # AI 助手提供的檔案
└── metadata/               # session 相關的 metadata
```

### 協作支援
- 多個 client 可共用 session 進行協作診斷
- 用途：比較不同裝置的設定差異、環境對比驗證
- 檔案命名包含 client ID 避免衝突
- 指令可廣播給 session 內所有 client

## 設計考量

### 技術選擇
- 選用 HTTP polling 而非 WebSocket 是為了最大相容性
- 被動式 Server 設計簡化了 Client 端的實作需求
- 實作簡單度優於效能最佳化

### Client 端實作範例
**目標環境：Windows IoT + PowerShell 5.1**
- PowerShell 5.1 是 Windows 環境最可靠的選擇
- 相容性要求：支援最基本的 loop 和 HTTP client 功能
- 主要用途：維運排查、程式部署驗證