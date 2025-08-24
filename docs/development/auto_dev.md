# Public-Tunnel 自動開發執行器

你是專案的自動化開發助手。請讀取以下文件並自動執行開發流程：

## 必讀文件
@docs/development/02_progress_tracking.md
@docs/development/01_feature_dependency_matrix.md
@docs/requirements/02_user_story.md
@docs/development/04_blocked_features.md
@docs/development/03_current_session.md

## 自動執行步驟

### 1. 任務選擇（在原專案中）
- 從進度文件找到第一個 "Not Started" 且無 blocking dependency 的 User Story
- 標記為 "in_progress" 
- 更新當前會話狀態
- 記錄選定的功能 ID（如：US-003）

### 2. 環境準備
- 建立功能分支：`git worktree add ../public-tunnel-dev-{功能ID} feature/{功能ID}`
- 切換到新 worktree 目錄
- 建立 venv：`python -m venv venv` 
- 啟用 venv：`source venv/bin/activate`
- 安裝依賴：`pip install -e ".[test]"`

### 3. 完整開發流程
按順序執行：
1. BDD 測試建立（使用 `@prompts/01_user-story-to-bdd-skeleton.md.prompt`）
2. API 骨架建立（使用 `@prompts/02_api-skeleton-creation.md.prompt`）
3. TDD 實作循環（使用 `@prompts/03_tdd-implementation-cycle.md.prompt`）
4. 最終審查（使用 `@prompts/05_final-commit-review.md.prompt`）

### 4. 完成與提交
- 在 worktree 中 commit 所有變更
- 回到原專案目錄：`cd ../public-tunnel`
- 合併功能分支：`git merge feature/{功能ID}` 或建立 PR
- 標記功能為 "completed"（更新進度文件）
- 清理 worktree：`git worktree remove ../public-tunnel-dev-{功能ID}`

### 5. 循環下一個功能
- 更新當前會話狀態
- 自動選擇下一個功能，重複流程

**遇到 blocking issue 時停止並報告。開始執行！**