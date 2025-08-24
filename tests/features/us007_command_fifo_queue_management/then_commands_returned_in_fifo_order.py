def execute(context):
    """
    Verify commands are returned in FIFO order
    
    This step verifies that:
    - Commands are returned in the same order they were submitted
    - First-in-first-out principle is maintained
    """
    from conftest import BDDPhase
    
    context.phase = BDDPhase.THEN
    
    # Verify we received the expected number of commands
    assert len(context.received_commands) == len(context.test_commands), \
        f"Expected {len(context.test_commands)} commands, but received {len(context.received_commands)}"
    
    # Verify FIFO order by comparing command content
    for i, received_command_info in enumerate(context.received_commands):
        expected_content = context.test_commands[i]
        received_command = received_command_info["command"]
        received_content = received_command.get("content")
        
        assert received_content == expected_content, \
            f"Command {i}: expected '{expected_content}', but got '{received_content}'"
    
    # Verify the order matches submission order
    print("FIFO order verification passed:")
    for i, received_command_info in enumerate(context.received_commands):
        print(f"  Position {i}: {received_command_info['command']['content']}")