def execute(context):
    """Given step: Set up commands by actually submitting them to the system"""
    
    # Set up test session and clients (use default session)
    context.session_id = "default"
    context.fast_client_id = "fast-client"  # For commands that complete quickly
    context.slow_client_id = "slow-client"  # For commands that may timeout
    
    # Register clients using context helper (common pattern)
    context.register_client(context.fast_client_id, context.session_id)
    context.register_client(context.slow_client_id, context.session_id)
    
    # Submit actual commands to establish real system state
    # Fast command - should complete quickly
    fast_response = context.test_client.post(
        f"/api/sessions/{context.session_id}/commands/submit",
        json={
            "command_content": "echo 'fast command'",
            "target_client_id": context.fast_client_id,
            "timeout_seconds": 30
        }
    )
    
    # Verify command submission succeeded and extract real command_id
    assert fast_response.status_code == 200, f"Fast command submission failed: {fast_response.status_code}"
    context.fast_command_id = fast_response.json()["command_id"]
    
    # Slow command - may timeout due to longer execution
    slow_response = context.test_client.post(
        f"/api/sessions/{context.session_id}/commands/submit", 
        json={
            "command_content": "sleep 3 && echo 'slow command'",
            "target_client_id": context.slow_client_id,
            "timeout_seconds": 30
        }
    )
    
    # Verify command submission succeeded and extract real command_id
    assert slow_response.status_code == 200, f"Slow command submission failed: {slow_response.status_code}"
    context.slow_command_id = slow_response.json()["command_id"]