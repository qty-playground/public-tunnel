def execute(context):
    """Then step: Verify unified API returns different execution states with consistent command-id indexing"""
    from conftest import BDDPhase
    
    context.phase = BDDPhase.THEN
    
    # Verify both completed and pending commands can be queried through the same unified API
    assert context.sync_query_response.status_code == 200, (
        f"Expected 200 OK for sync (completed) command result query, got {context.sync_query_response.status_code}. "
        f"Response: {context.sync_query_response.text}"
    )
    
    assert context.async_query_response.status_code == 200, (
        f"Expected 200 OK for async (pending) command result query, got {context.async_query_response.status_code}. "
        f"Response: {context.async_query_response.text}"
    )
    
    # Extract results from unified query API
    sync_unified_result = context.sync_query_response.json()
    async_unified_result = context.async_query_response.json()
    
    # Verify command-id indexing works for both execution states
    assert sync_unified_result["command_id"] == context.sync_command_id, (
        f"Sync result should have command_id {context.sync_command_id}, got {sync_unified_result.get('command_id')}"
    )
    
    assert async_unified_result["command_id"] == context.async_command_id, (
        f"Async result should have command_id {context.async_command_id}, got {async_unified_result.get('command_id')}"
    )
    
    # Verify unified response format is consistent regardless of execution state
    required_fields = ["command_id", "execution_status", "client_id", "session_id", "submitted_at"]
    
    for field in required_fields:
        assert field in sync_unified_result, f"Sync result missing required field: {field}"
        assert field in async_unified_result, f"Async result missing required field: {field}"
    
    # Key verification: Different execution states show appropriate status
    assert sync_unified_result["execution_status"] == "completed", (
        f"Sync command should show completed status, got {sync_unified_result['execution_status']}"
    )
    
    assert async_unified_result["execution_status"] == "pending", (
        f"Async command should show pending status, got {async_unified_result['execution_status']}"
    )
    
    # Verify completed command has result content while pending command doesn't
    assert sync_unified_result.get("result_content") is not None, (
        f"Sync (completed) command should have result_content, got {sync_unified_result.get('result_content')}"
    )
    
    assert async_unified_result.get("result_content") is None, (
        f"Async (pending) command should not have result_content yet, got {async_unified_result.get('result_content')}"
    )
    
    # Verify that both results belong to correct clients and session
    assert sync_unified_result["client_id"] == context.sync_client_id, (
        f"Sync result should be from client {context.sync_client_id}, got {sync_unified_result['client_id']}"
    )
    
    assert async_unified_result["client_id"] == context.async_client_id, (
        f"Async result should be from client {context.async_client_id}, got {async_unified_result['client_id']}"
    )
    
    assert sync_unified_result["session_id"] == context.session_id, (
        f"Sync result should be in session {context.session_id}, got {sync_unified_result['session_id']}"
    )
    
    assert async_unified_result["session_id"] == context.session_id, (
        f"Async result should be in session {context.session_id}, got {async_unified_result['session_id']}"
    )
    
    # Core US-021 verification: Same API endpoint works for both completed and pending results
    # This demonstrates the unified query mechanism regardless of command execution state