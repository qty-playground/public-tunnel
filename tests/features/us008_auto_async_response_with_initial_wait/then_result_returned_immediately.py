from conftest import BDDPhase

def execute(context):
    """Verify that the result was returned immediately (fast execution scenario)"""
    context.phase = BDDPhase.THEN
    
    # Verify command submission was successful
    assert context.submission_result["status_code"] in [200, 201], \
        f"Expected 200/201, got {context.submission_result['status_code']}"
    
    response_data = context.submission_result["response_data"]
    assert response_data is not None, "Expected response data for immediate result"
    
    # For immediate response, we should get the actual result, not just a command-id
    # The response should contain the execution result directly
    assert "result" in response_data, "Expected immediate result in response"
    assert response_data["result"] is not None, "Expected non-null immediate result"
    
    # Should NOT be in async mode (no command_id for polling)
    assert "command_id" not in response_data or response_data.get("async_mode") is False, \
        "Fast command should not return command_id for polling"