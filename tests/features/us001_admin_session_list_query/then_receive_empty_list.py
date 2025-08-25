def execute(context):
    # Verify that response shows minimal sessions (just default)
    assert context.response.status_code == 200, f"Expected 200 OK, got {context.response.status_code}"
    
    response_data = context.response.json()
    assert "sessions" in response_data, "Response should contain 'sessions' field"
    
    # System should have at least the default session
    assert len(response_data["sessions"]) >= 1, "System should have at least default session"
    assert response_data["total_sessions"] >= 1, "Total sessions should be at least 1"
    
    # Check that we have the default session
    default_session_exists = any(session["default_session"] for session in response_data["sessions"])
    assert default_session_exists, "Default session should exist in the system"