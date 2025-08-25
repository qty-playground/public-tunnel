def execute(context):
    # Verify that response contains all sessions
    assert context.response.status_code == 200, f"Expected 200 OK, got {context.response.status_code}"
    
    response_data = context.response.json()
    assert "sessions" in response_data, "Response should contain 'sessions' field"
    assert "total_sessions" in response_data, "Response should contain 'total_sessions' field"  
    assert "queried_at" in response_data, "Response should contain 'queried_at' field"
    
    # If we expected sessions to exist, verify they're in the response
    if context.expected_sessions_exist:
        assert len(response_data["sessions"]) > 0, "Expected sessions to exist but got empty list"
    
    # Store response for further validation
    context.session_list_response = response_data