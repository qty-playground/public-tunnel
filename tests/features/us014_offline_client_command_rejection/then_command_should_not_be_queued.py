def execute(context):
    """Then step: 驗證指令沒有被加到佇列中"""
    from conftest import BDDPhase
    
    context.phase = BDDPhase.THEN
    
    # 驗證指令沒有被加到佇列中
    # 嘗試讓 offline client 進行 polling，應該不會收到任何指令
    
    # 先讓 client 重新上線（透過 polling 更新 last_seen 時間）
    poll_response = context.test_client.get(
        f"/api/sessions/{context.session_id}/clients/{context.offline_client_id}/commands/poll"
    )
    
    # 檢查 polling 回應狀態
    assert poll_response.status_code == 200, f"Expected 200 for polling, got {poll_response.status_code}"
    
    poll_data = poll_response.json()
    
    # 驗證沒有待處理的指令
    # 根據 US-007 和 US-009，如果沒有指令，應該回傳空的回應或明確表示沒有指令
    if "command" in poll_data:
        # 如果有 command 欄位，它應該是 null 或不存在
        assert poll_data["command"] is None, (
            f"Expected no queued commands for offline client, but found: {poll_data['command']}"
        )
    elif "commands" in poll_data:
        # 如果是 commands 陣列，應該是空的
        assert len(poll_data["commands"]) == 0, (
            f"Expected no queued commands for offline client, but found {len(poll_data['commands'])} commands"
        )
    
    # 進一步驗證：檢查佇列大小
    from public_tunnel.dependencies.providers import get_command_queue_manager
    queue_manager = get_command_queue_manager()
    
    # 獲取該 client 的佇列大小
    queue_size = queue_manager.get_queue_size_for_client(
        session_id=context.session_id,
        client_id=context.offline_client_id
    )
    
    # 佇列應該是空的
    assert queue_size == 0, (
        f"Expected empty queue for offline client, but found {queue_size} commands in queue"
    )