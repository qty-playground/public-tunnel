def execute(context):
    """
    Verify that exactly one command was returned in the API response
    
    This step validates that:
    1. The API call was successful (HTTP 200)
    2. The response contains exactly one command
    3. The command data matches expected format
    4. The response indicates proper queue state
    """
    # Verify successful API response
    assert context.api_response.status_code == 200, \
        f"Expected HTTP 200, got {context.api_response.status_code}"
    
    # Verify response data exists
    assert context.response_data is not None, \
        "Expected response data but got None"
    
    # Verify that exactly one command was returned
    assert context.response_data.get("command") is not None, \
        "Expected command data in response but got None"
    
    # Verify command structure contains required fields
    command = context.response_data["command"]
    required_fields = ["command_id", "content", "target_client", "session_id"]
    
    for field in required_fields:
        assert field in command, \
            f"Expected '{field}' in command data but not found"
    
    # Verify the command is the first one from our test data (FIFO order)
    expected_first_command = context.test_commands[0]
    assert command["command_id"] == expected_first_command.command_id, \
        f"Expected command_id {expected_first_command.command_id}, got {command['command_id']}"
    assert command["content"] == expected_first_command.content, \
        f"Expected content {expected_first_command.content}, got {command['content']}"
    
    # Verify queue state indicators
    assert "has_more_commands" in context.response_data, \
        "Expected has_more_commands field in response"
    assert "queue_size" in context.response_data, \
        "Expected queue_size field in response"
    
    # Should indicate more commands remain (we started with 3, got 1)
    assert context.response_data["has_more_commands"] == True, \
        "Expected has_more_commands to be True since we had 3 commands initially"
    assert context.response_data["queue_size"] == 2, \
        f"Expected queue_size to be 2, got {context.response_data['queue_size']}"