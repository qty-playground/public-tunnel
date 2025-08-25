def execute(context):
    """Then step: Verify unified API returns results with command-id indexing"""
    from conftest import BDDPhase
    
    context.phase = BDDPhase.THEN
    
    # TDD Phase: Expect successful result queries with command-id indexing
    assert context.fast_response.status_code == 200, (
        f"Expected 200 OK for fast command result query, got {context.fast_response.status_code}. "
        f"Response: {context.fast_response.text}"
    )
    
    assert context.slow_response.status_code == 200, (
        f"Expected 200 OK for slow command result query, got {context.slow_response.status_code}. "
        f"Response: {context.slow_response.text}"
    )
    
    # Verify both results have command-id indexing
    fast_result = context.fast_response.json()
    slow_result = context.slow_response.json()
    
    assert fast_result["command_id"] == context.fast_command_id, (
        f"Fast result should have command_id {context.fast_command_id}, got {fast_result.get('command_id')}"
    )
    
    assert slow_result["command_id"] == context.slow_command_id, (
        f"Slow result should have command_id {context.slow_command_id}, got {slow_result.get('command_id')}"
    )