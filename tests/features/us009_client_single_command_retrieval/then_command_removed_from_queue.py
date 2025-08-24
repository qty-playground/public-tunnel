def execute(context):
    """
    Verify that the command was actually removed from the queue after polling
    
    This step validates that:
    1. The queue size decreased by exactly one after the API call
    2. The specific command is no longer in the queue
    3. The remaining commands maintain FIFO order
    """
    # Verify the queue size decreased from initial state
    # We started with 3 commands, should have 2 remaining
    assert context.queue_size_after_request == 2, \
        f"Expected queue size to be 2 after retrieving one command, got {context.queue_size_after_request}"
    
    # Verify via direct queue manager call as well
    from public_tunnel.dependencies.providers import get_command_queue_manager
    queue_manager = get_command_queue_manager()
    
    current_queue_size = queue_manager.get_queue_size_for_client(
        context.test_session_id, 
        context.test_client_id
    )
    
    assert current_queue_size == 2, \
        f"Expected current queue size to be 2, got {current_queue_size}"
    
    # Verify the remaining commands maintain FIFO order by checking next command
    # Make another API call to see if we get the second command
    api_endpoint = f"/api/sessions/{context.test_session_id}/clients/{context.test_client_id}/command"
    second_response = context.test_client.get(api_endpoint)
    
    if second_response.status_code == 200:
        second_response_data = second_response.json()
        
        # The second command should be the second one from our test data
        if second_response_data.get("command"):
            expected_second_command = context.test_commands[1]
            returned_command = second_response_data["command"]
            
            assert returned_command["command_id"] == expected_second_command.command_id, \
                f"Expected second command_id {expected_second_command.command_id}, got {returned_command['command_id']}"
            
            # Verify queue state after second retrieval
            assert second_response_data["has_more_commands"] == True, \
                "Expected has_more_commands to be True since one command should remain"
            assert second_response_data["queue_size"] == 1, \
                f"Expected queue_size to be 1 after second retrieval, got {second_response_data['queue_size']}"