def execute(context):
    """Then step: Verify sync and async command results can be queried through same unified API"""
    from conftest import BDDPhase
    
    context.phase = BDDPhase.THEN
    
    # API Skeleton Phase: Both responses should use the same endpoint structure
    sync_url_parts = context.sync_query_response.url.path.split('/')
    async_url_parts = context.async_query_response.url.path.split('/')
    
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
    assert context.sync_query_response.status_code == context.async_query_response.status_code == 200, (
        f"Both sync and async queries should return 200 OK, got sync: {context.sync_query_response.status_code}, async: {context.async_query_response.status_code}"
    )
    
    # Verify both responses have the same structure (unified API format)
    sync_result = context.sync_query_response.json()
    async_result = context.async_query_response.json()
    
    # Both results should have the same unified response structure
    required_fields = ["command_id", "execution_status", "client_id", "session_id", "submitted_at"]
    
    for field in required_fields:
        assert field in sync_result, f"Sync result should have field '{field}'"
        assert field in async_result, f"Async result should have field '{field}'"
    
    # Verify results can be distinguished by command_id, not execution state
    assert sync_result["command_id"] == context.sync_command_id, (
        f"Sync command should have command_id '{context.sync_command_id}', got '{sync_result.get('command_id')}'"
    )
    assert async_result["command_id"] == context.async_command_id, (
        f"Async command should have command_id '{context.async_command_id}', got '{async_result.get('command_id')}'"
    )