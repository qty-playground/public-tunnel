def execute(context):
    """
    Verify each polling returns only one command
    
    This step verifies that:
    - Each successful polling response contains exactly one command
    - No polling returns multiple commands at once
    - Single command per polling constraint is maintained
    """
    from conftest import BDDPhase
    
    context.phase = BDDPhase.THEN
    
    # Verify each received command corresponds to exactly one polling attempt
    for received_command_info in context.received_commands:
        command = received_command_info["command"]
        
        # Verify the command is a single command (not an array)
        assert isinstance(command, dict), \
            f"Expected single command object, but got {type(command)}"
        
        # Verify command has required fields
        assert "content" in command, "Command missing 'content' field"
        assert "command_id" in command, "Command missing 'command_id' field"
    
    # Verify that we made exactly the number of successful polling attempts 
    # as commands received (each polling should return exactly one command)
    successful_polls = len([cmd for cmd in context.received_commands if cmd["command"]])
    total_commands = len(context.received_commands)
    
    assert successful_polls == total_commands, \
        f"Inconsistent polling results: {successful_polls} successful polls vs {total_commands} commands"
    
    print("Single command per polling verification passed:")
    for i, received_command_info in enumerate(context.received_commands):
        print(f"  Polling attempt {received_command_info['attempt']}: 1 command returned")