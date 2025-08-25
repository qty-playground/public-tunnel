from conftest import BDDPhase

def execute(context):
    """Set up a command submission scenario for auto async response testing"""
    context.phase = BDDPhase.GIVEN
    
    # Set up test environment
    context.session_id = "test-session-auto-async"
    context.client_id = "test-client-auto-async" 
    context.command_content = "echo 'test command'"
    
    # Register client first (based on existing patterns)
    client_response = context.test_client.post(
        f"/api/sessions/{context.session_id}/poll",
        json={"client_id": context.client_id}
    )
    assert client_response.status_code == 200
    
    # Prepare command submission data (using correct request format)
    context.command_submission_data = {
        "command_content": context.command_content,
        "target_client_id": context.client_id
    }