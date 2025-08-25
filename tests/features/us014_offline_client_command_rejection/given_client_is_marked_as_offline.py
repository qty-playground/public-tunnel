def execute(context):
    """Given step: 設定一個 client 為 offline 狀態"""
    from conftest import BDDPhase
    
    context.phase = BDDPhase.GIVEN
    
    # 設定測試數據
    context.offline_client_id = "offline-client-001"
    context.command_content = "echo 'test command for offline client'"
    context.session_id = "default"
    
    # 首先，讓 client 透過 polling 註冊到 session（這樣才不會被 US-013 攔截）
    context.test_client.get(
        f"/api/sessions/{context.session_id}/clients/{context.offline_client_id}/commands/poll"
    )
    
    # 然後透過手動設定 last_seen 時間將 client 標記為 offline
    # 這模擬了 client 停止 polling 並超過 threshold 時間的情況
    from public_tunnel.dependencies.providers import get_client_presence_tracker
    presence_tracker = get_client_presence_tracker()
    
    # 手動將 client 的 last_seen 時間設定為很久以前，確保它被標記為 offline
    import datetime
    very_old_time = datetime.datetime.now() - datetime.timedelta(seconds=300)  # 5 minutes ago
    
    # 使用正確的 API 更新 client 的 last_seen 時間為很久以前
    presence_tracker.update_client_last_seen(
        client_id=context.offline_client_id,
        session_id=context.session_id,
        timestamp=very_old_time
    )
    
    # 執行強制離線檢查，確保 client 被正確標記為 offline
    context.test_client.post(f"/api/sessions/{context.session_id}/offline-status/force-check")