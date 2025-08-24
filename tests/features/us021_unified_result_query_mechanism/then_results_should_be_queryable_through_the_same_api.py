def execute(context):
    """Then step: Verify both sync and async results can be queried through same API"""
    from conftest import BDDPhase
    
    context.phase = BDDPhase.THEN
    
    # API Skeleton Phase: Both responses should use the same endpoint structure
    sync_url_parts = context.sync_response.url.path.split('/')
    async_url_parts = context.async_response.url.path.split('/')
    
    # Verify both use the same API endpoint pattern
    assert sync_url_parts[:-1] == async_url_parts[:-1], (
        "Sync and async commands should use the same API endpoint pattern"
    )
    
    # Verify the endpoint includes sessions, results and command_id structure
    expected_pattern = ['', 'api', 'sessions', context.session_id, 'results']
    assert sync_url_parts[:-1] == expected_pattern, (
        f"API pattern should be {expected_pattern}, got {sync_url_parts[:-1]}"
    )
    
    # Verify command_id is the differentiator
    assert sync_url_parts[-1] == context.sync_command_id
    assert async_url_parts[-1] == context.async_command_id
    
    # TDD Phase: Both should return successful responses (200 OK)
    assert context.sync_response.status_code == context.async_response.status_code == 200, (
        f"Both sync and async queries should return 200 OK, got sync: {context.sync_response.status_code}, async: {context.async_response.status_code}"
    )
    
    # Verify both responses have the same structure (unified API format)
    sync_result = context.sync_response.json()
    async_result = context.async_response.json()
    
    # Both results should have the same unified response structure
    required_fields = ["command_id", "execution_mode", "execution_status", "client_id", "session_id", "submitted_at"]
    
    for field in required_fields:
        assert field in sync_result, f"Sync result should have field '{field}'"
        assert field in async_result, f"Async result should have field '{field}'"
    
    # Verify execution modes are correctly identified
    assert sync_result["execution_mode"] == "sync", (
        f"Sync command should have execution_mode 'sync', got '{sync_result.get('execution_mode')}'"
    )
    assert async_result["execution_mode"] == "async", (
        f"Async command should have execution_mode 'async', got '{async_result.get('execution_mode')}'"
    )