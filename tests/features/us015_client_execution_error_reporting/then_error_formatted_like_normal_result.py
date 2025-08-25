def execute(context):
    """Then step: Verify that the error result has the same format structure as success results"""
    from conftest import BDDPhase
    
    context.phase = BDDPhase.THEN
    
    # Error reporting should return successful HTTP status (200 OK) when error is properly recorded
    assert context.error_report_response.status_code == 200, (
        f"Error reporting should return 200 OK, got {context.error_report_response.status_code}"
    )
    
    # The response should have a confirmation format that matches success result submissions
    error_response = context.error_report_response.json()
    
    # Expected fields that should be consistent with success result format
    expected_fields = ["command_id", "session_id", "execution_status"]
    
    for field in expected_fields:
        assert field in error_response, (
            f"Error response should have field '{field}' like normal results"
        )
    
    # Verify specific error formatting requirements
    assert error_response["command_id"] == context.command_id, (
        f"Response should include command_id '{context.command_id}', got '{error_response.get('command_id')}'"
    )
    
    assert error_response["session_id"] == context.session_id, (
        f"Response should include session_id '{context.session_id}', got '{error_response.get('session_id')}'"
    )
    
    assert error_response["execution_status"] == "failed", (
        f"Response should show execution_status as 'failed', got '{error_response.get('execution_status')}'"
    )