def execute(context):
    """Then step: Verify that AI assistant can query the error result using the same API as success results"""
    from conftest import BDDPhase
    
    context.phase = BDDPhase.THEN
    
    # Use query response from WHEN phase
    query_response = context.error_query_response
    
    # Verify query is successful
    assert query_response.status_code == 200, (
        f"Error query should return 200 OK, got {query_response.status_code}"
    )
    
    # The response should be in unified result format
    error_result = query_response.json()
    
    # Verify unified result structure fields
    unified_fields = [
        "command_id", "execution_mode", "execution_status", 
        "client_id", "session_id", "submitted_at"
    ]
    
    for field in unified_fields:
        assert field in error_result, (
            f"Error query result should have unified field '{field}'"
        )
    
    # Verify error-specific data
    assert error_result["command_id"] == context.command_id, (
        f"Queried error should have command_id '{context.command_id}', got '{error_result.get('command_id')}'"
    )
    
    assert error_result["execution_status"] == "failed", (
        f"Queried error should have execution_status 'failed', got '{error_result.get('execution_status')}'"
    )
    
    assert error_result["error_message"] == context.error_message, (
        f"Queried error should contain error_message '{context.error_message}', got '{error_result.get('error_message')}'"
    )
    
    # Verify error result content is None (no result for failed commands)
    assert error_result.get("result_content") is None, (
        f"Failed command should have no result_content, got '{error_result.get('result_content')}'"
    )