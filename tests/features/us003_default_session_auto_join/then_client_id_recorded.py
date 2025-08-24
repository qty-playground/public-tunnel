def execute(context):
    # TDD phase: Verify client registration
    response_data = context.response.json()
    assert response_data["client_id"] == context.client_id, (
        f"Expected client_id {context.client_id}, got {response_data.get('client_id')}"
    )
    assert response_data["registration_status"] in ["new", "existing"], (
        f"Expected registration_status to be 'new' or 'existing', got {response_data.get('registration_status')}"
    )