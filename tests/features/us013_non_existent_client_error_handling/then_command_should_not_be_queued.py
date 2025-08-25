def execute(context):
    """Then step: 驗證指令沒有被放入佇列"""
    from conftest import BDDPhase
    from public_tunnel.dependencies.providers import get_command_queue_manager
    
    context.phase = BDDPhase.THEN
    
    # 取得 command queue manager 實例
    queue_manager = get_command_queue_manager()
    
    # 驗證不存在的 client 沒有任何指令被排入佇列
    queue_size = queue_manager.get_queue_size_for_client(
        session_id=context.session_id,
        client_id=context.non_existent_client_id
    )
    
    assert queue_size == 0, (
        f"Commands should not be queued for non-existent client, "
        f"but found {queue_size} commands in queue"
    )
    
    # 進一步驗證：檢查整個 session 中所有有指令的 client
    clients_with_commands = queue_manager.get_all_clients_with_commands_in_session(context.session_id)
    
    assert context.non_existent_client_id not in clients_with_commands, (
        f"Non-existent client '{context.non_existent_client_id}' should not be in the list "
        f"of clients with commands: {clients_with_commands}"
    )