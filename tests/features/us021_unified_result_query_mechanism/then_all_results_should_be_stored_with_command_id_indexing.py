def execute(context):
    """Then step: Verify unified API returns results with command-id indexing"""
    from conftest import BDDPhase
    
    context.phase = BDDPhase.THEN
    
    # TDD Phase: Expect successful result queries with command-id indexing
    assert context.sync_response.status_code == 200, (
        f"Expected 200 OK for sync command result query, got {context.sync_response.status_code}. "
        f"Response: {context.sync_response.text}"
    )
    
    assert context.async_response.status_code == 200, (
        f"Expected 200 OK for async command result query, got {context.async_response.status_code}. "
        f"Response: {context.async_response.text}"
    )
    
    # Verify both results have command-id indexing
    sync_result = context.sync_response.json()
    async_result = context.async_response.json()
    
    assert sync_result["command_id"] == context.sync_command_id, (
        f"Sync result should have command_id {context.sync_command_id}, got {sync_result.get('command_id')}"
    )
    
    assert async_result["command_id"] == context.async_command_id, (
        f"Async result should have command_id {context.async_command_id}, got {async_result.get('command_id')}"
    )