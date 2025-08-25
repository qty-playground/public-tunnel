def execute(context):
    # Verify that each session includes basic metadata
    session_list = context.session_list_response["sessions"]
    
    for session in session_list:
        # Verify each session has required metadata fields
        assert "session_id" in session, "Session should have session_id"
        assert "client_count" in session, "Session should have client_count"
        assert "created_at" in session, "Session should have created_at"
        assert "default_session" in session, "Session should have default_session flag"