def execute(context):
    # Verify that no session information is revealed
    response_data = context.response.json()
    
    # Should not contain session list or session information
    assert "sessions" not in response_data, "Response should not contain session information"
    assert "total_sessions" not in response_data, "Response should not contain session count"
    
    # Should contain error message instead
    assert "detail" in response_data, "Response should contain error detail"