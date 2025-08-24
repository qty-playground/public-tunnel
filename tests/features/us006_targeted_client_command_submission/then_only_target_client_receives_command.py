def execute(context):
    """
    Verify that only the target client will receive the command
    
    During API Skeleton phase, this is verified by the 501 response
    indicating the queue isolation logic is planned but not yet implemented.
    """
    from conftest import BDDPhase
    
    context.phase = BDDPhase.THEN
    
    # GREEN Stage 1: Basic verification that command is targeted correctly
    # The 200 status indicates command was accepted for the specific client
    assert context.status_code == 200, (
        f"Expected successful response for targeted command submission"
    )
    
    # Verify the command is associated with the correct target client
    assert context.response_data["target_client_id"] == context.target_client_id, (
        f"Command should be targeted to client {context.target_client_id}"
    )
    
    # GREEN Stage 2: Verify actual queue isolation
    # Get the command queue manager to verify isolation
    from public_tunnel.dependencies.providers import get_command_queue_manager
    
    queue_manager = get_command_queue_manager()
    
    # Verify target client has exactly 1 command in queue
    target_queue_size = queue_manager.get_queue_size_for_client(
        context.session_id, 
        context.target_client_id
    )
    assert target_queue_size == 1, (
        f"Target client {context.target_client_id} should have 1 command in queue, "
        f"got {target_queue_size}"
    )
    
    # Verify other clients in same session have no commands
    # Test with a different client ID
    other_client_id = "client-999"  # Different from target client
    other_queue_size = queue_manager.get_queue_size_for_client(
        context.session_id,
        other_client_id
    )
    assert other_queue_size == 0, (
        f"Other client {other_client_id} should have 0 commands in queue, "
        f"got {other_queue_size}"
    )
    
    # Verify only the target client shows up as having commands
    clients_with_commands = queue_manager.get_all_clients_with_commands_in_session(
        context.session_id
    )
    assert context.target_client_id in clients_with_commands, (
        f"Target client {context.target_client_id} should be in clients with commands"
    )
    assert other_client_id not in clients_with_commands, (
        f"Other client {other_client_id} should not be in clients with commands"
    )