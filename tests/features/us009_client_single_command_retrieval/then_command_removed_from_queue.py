def execute(context):
    """
    Verify that the retrieved command was actually removed from the queue
    
    We verify removal by making a second READ-ONLY API call to check:
    1. The queue size decreased (internal state verification)  
    2. The next command is the second one from our test data (FIFO verification)
    3. The first command is truly gone (removal verification)
    
    This uses GET API calls for verification, which is appropriate in Then steps.
    """
    # First verify through service layer that queue size decreased
    from public_tunnel.dependencies.providers import get_command_queue_manager
    queue_manager = get_command_queue_manager()
    
    current_queue_size = queue_manager.get_queue_size_for_client(
        context.test_session_id, 
        context.test_client_id
    )
    
    assert current_queue_size == 2, \
        f"Command was not removed: expected queue size 2, got {current_queue_size}"
    
    # Then verify through API layer (external behavior verification)
    # Make a second GET request to confirm FIFO order and removal
    api_endpoint = f"/api/sessions/{context.test_session_id}/clients/{context.test_client_id}/command"
    second_response = context.test_client.get(api_endpoint)
    
    assert second_response.status_code == 200, \
        f"Second API call failed with status {second_response.status_code}"
    
    second_response_data = second_response.json()
    
    # Verify we get the second command (proving first was removed and FIFO works)
    assert second_response_data.get("command") is not None, \
        "Expected to receive second command but got None"
    
    expected_second_command = context.test_commands[1]  # Should be "ls -la"
    returned_command = second_response_data["command"]
    
    assert returned_command["command_id"] == expected_second_command.command_id, \
        f"FIFO order broken: expected {expected_second_command.command_id}, got {returned_command['command_id']}"
    assert returned_command["content"] == "ls -la", \
        f"Expected second command 'ls -la', got '{returned_command['content']}'"
    
    # Verify final queue state
    assert second_response_data["queue_size"] == 1, \
        f"Expected final queue size 1, got {second_response_data['queue_size']}"
    assert second_response_data["has_more_commands"] == True, \
        "Expected has_more_commands=True since one command should remain"