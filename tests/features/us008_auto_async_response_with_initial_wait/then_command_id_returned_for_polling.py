from conftest import BDDPhase

def execute(context):
    """Verify that a command-id was returned for polling (slow execution scenario)"""
    context.phase = BDDPhase.THEN
    
    # Verify command submission was successful
    assert context.submission_result["status_code"] in [200, 201], \
        f"Expected 200/201, got {context.submission_result['status_code']}"
    
    response_data = context.submission_result["response_data"]
    assert response_data is not None, "Expected response data for async mode"
    
    # For async response, we should get a command-id to poll for results
    assert "command_id" in response_data, "Expected command_id for polling in async mode"
    assert response_data["command_id"] is not None, "Expected non-null command_id"
    
    # Should be in async mode (no immediate result)
    assert response_data.get("async_mode") is True, "Slow command should be in async mode"
    assert "result" not in response_data or response_data["result"] is None, \
        "Async mode should not return immediate result"
    
    # Verify we can use the command_id to query results later (using existing US-021 API)
    command_id = response_data["command_id"]
    query_response = context.test_client.get(
        f"/api/sessions/{context.session_id}/results/{command_id}"
    )
    
    # The query should be successful (though result might still be pending)
    assert query_response.status_code in [200, 202], \
        f"Command result query should be accessible, got {query_response.status_code}"