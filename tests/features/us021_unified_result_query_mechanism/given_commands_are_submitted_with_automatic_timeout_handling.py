def execute(context):
    """Given step: Set up sync and async command states by simulating client response patterns"""
    from conftest import BDDPhase
    
    context.phase = BDDPhase.GIVEN
    
    # Set up test session and clients (use default session)
    context.session_id = "default"
    context.sync_client_id = "sync-client"  # For synchronous (completed) execution
    context.async_client_id = "async-client"  # For asynchronous (pending) execution
    
    # Register clients using context helper (common pattern)
    context.register_client(context.sync_client_id, context.session_id)
    context.register_client(context.async_client_id, context.session_id)
    
    # === SYNC CASE: Submit command and simulate immediate client completion ===
    # Submit command for sync client
    sync_response = context.test_client.post(
        f"/api/sessions/{context.session_id}/commands/submit",
        json={
            "command_content": "echo 'sync command'",
            "target_client_id": context.sync_client_id,
            "timeout_seconds": 30
        }
    )
    
    assert sync_response.status_code == 200, f"Sync command submission failed: {sync_response.status_code}"
    context.sync_command_id = sync_response.json()["command_id"]
    
    # Simulate client completing the command immediately (sync behavior)
    sync_result_response = context.test_client.post(
        f"/api/sessions/{context.session_id}/results",
        json={
            "command_id": context.sync_command_id,
            "execution_status": "completed",
            "result_content": "sync command completed successfully"
        }
    )
    
    assert sync_result_response.status_code == 200, f"Sync result submission failed: {sync_result_response.status_code}"
    
    # === ASYNC CASE: Submit command but client hasn't completed yet ===
    # Submit command for async client
    async_response = context.test_client.post(
        f"/api/sessions/{context.session_id}/commands/submit",
        json={
            "command_content": "sleep 5 && echo 'async command'",
            "target_client_id": context.async_client_id,
            "timeout_seconds": 30
        }
    )
    
    assert async_response.status_code == 200, f"Async command submission failed: {async_response.status_code}"
    context.async_command_id = async_response.json()["command_id"]
    
    # Note: We deliberately don't submit result for async command to simulate pending state
    # This represents the real-world scenario where async command is still executing