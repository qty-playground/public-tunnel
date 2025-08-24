def execute(context):
    # TDD phase: Verify actual session assignment
    assert context.response.status_code == 200, (
        f"Expected successful response, got {context.response.status_code}. "
        f"Response: {context.response.text}"
    )
    
    response_data = context.response.json()
    assert response_data["session_id"] == "default", (
        f"Expected client to be assigned to 'default' session, got {response_data.get('session_id')}"
    )