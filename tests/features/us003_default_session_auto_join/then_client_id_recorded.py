def execute(context):
    # TDD phase: Verify client registration with dual verification (API + State)
    
    # 1. API level verification - HTTP response correctness
    response_data = context.response.json()
    assert response_data["client_id"] == context.client_id, (
        f"Expected client_id {context.client_id}, got {response_data.get('client_id')}"
    )
    assert response_data["registration_status"] in ["new", "existing"], (
        f"Expected registration_status to be 'new' or 'existing', got {response_data.get('registration_status')}"
    )
    
    # 2. State level verification - Internal repository state
    from public_tunnel.dependencies.providers import get_session_repository
    session_repo = get_session_repository()
    
    # Verify client is actually recorded in the session
    default_session_id = "default"
    assert session_repo.is_client_in_session(default_session_id, context.client_id), (
        f"Client {context.client_id} should be recorded in session {default_session_id}"
    )
    
    # Verify session info is updated correctly
    session_info = session_repo.get_session_info(default_session_id)
    assert session_info is not None, "Default session should exist"
    assert session_info.client_count >= 1, "Session should have at least one client"
    
    # Verify client list contains our client
    clients_in_session = session_repo.get_clients_in_session(default_session_id)
    assert context.client_id in clients_in_session, (
        f"Client {context.client_id} should be in the session client list"
    )