from conftest import BDDPhase
from fastapi import status

def execute(context):
    """Verify that offline clients do not receive new commands"""
    context.phase = BDDPhase.THEN
    
    # Step 1: Try to submit a command targeting the offline client
    command_submission_response = context.test_client.post(
        f"/api/sessions/{context.session_id}/commands",
        json={
            "command": "echo 'test command for offline client'",
            "target_client": context.client_id
        }
    )
    
    # GREEN Stage 2: Detailed verification logic
    
    # API level verification - command submission should be rejected
    assert command_submission_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, (
        f"Command submission to offline client should be rejected with 422, "
        f"but got status {command_submission_response.status_code}"
    )
    
    error_response = command_submission_response.json()
    assert "detail" in error_response, "Error response should contain detail message"
    
    error_message = error_response["detail"]
    
    # Verify error message indicates client offline status
    assert "offline client" in error_message.lower() or "offline" in error_message.lower(), (
        f"Error message should indicate client is offline, but got: {error_message}"
    )
    
    assert context.client_id in error_message, (
        f"Error message should mention the client ID {context.client_id}, but got: {error_message}"
    )
    
    # Verify the error explains that clients must be online to receive commands
    assert "must be online" in error_message.lower() or "online to receive" in error_message.lower(), (
        f"Error message should explain client must be online for commands, but got: {error_message}"
    )
    
    # Additional verification: ensure no command_id is returned in error case
    assert "command_id" not in error_response, (
        "Failed command submission should not return a command_id"
    )