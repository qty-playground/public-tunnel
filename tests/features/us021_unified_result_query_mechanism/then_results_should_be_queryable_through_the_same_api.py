def execute(context):
    """Then step: Verify all command results can be queried through same API regardless of execution time"""
    from conftest import BDDPhase
    
    context.phase = BDDPhase.THEN
    
    # API Skeleton Phase: Both responses should use the same endpoint structure
    fast_url_parts = context.fast_response.url.path.split('/')
    slow_url_parts = context.slow_response.url.path.split('/')
    
    # Verify both use the same API endpoint pattern
    assert fast_url_parts[:-1] == slow_url_parts[:-1], (
        "Fast and slow commands should use the same API endpoint pattern"
    )
    
    # Verify the endpoint includes sessions, results and command_id structure
    expected_pattern = ['', 'api', 'sessions', context.session_id, 'results']
    assert fast_url_parts[:-1] == expected_pattern, (
        f"API pattern should be {expected_pattern}, got {fast_url_parts[:-1]}"
    )
    
    # Verify command_id is the differentiator
    assert fast_url_parts[-1] == context.fast_command_id
    assert slow_url_parts[-1] == context.slow_command_id
    
    # TDD Phase: Both should return successful responses (200 OK)
    assert context.fast_response.status_code == context.slow_response.status_code == 200, (
        f"Both fast and slow queries should return 200 OK, got fast: {context.fast_response.status_code}, slow: {context.slow_response.status_code}"
    )
    
    # Verify both responses have the same structure (unified API format)
    fast_result = context.fast_response.json()
    slow_result = context.slow_response.json()
    
    # Both results should have the same unified response structure
    required_fields = ["command_id", "execution_status", "client_id", "session_id", "submitted_at"]
    
    for field in required_fields:
        assert field in fast_result, f"Fast result should have field '{field}'"
        assert field in slow_result, f"Slow result should have field '{field}'"
    
    # Verify results can be distinguished by command_id, not execution mode
    assert fast_result["command_id"] == context.fast_command_id, (
        f"Fast command should have command_id '{context.fast_command_id}', got '{fast_result.get('command_id')}'"
    )
    assert slow_result["command_id"] == context.slow_command_id, (
        f"Slow command should have command_id '{context.slow_command_id}', got '{slow_result.get('command_id')}'"
    )