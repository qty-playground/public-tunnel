def execute(context):
    """
    Simulate client polling for commands using US-007 FIFO polling API
    
    This step calls the FIFO polling endpoint multiple times to:
    - Retrieve all queued commands one by one
    - Record the order in which commands are returned
    """
    from conftest import BDDPhase
    
    context.phase = BDDPhase.WHEN
    
    # Use US-007 FIFO polling API endpoint
    api_endpoint = f"/api/sessions/{context.session_id}/clients/{context.target_client_id}/commands/poll"
    
    context.polling_results = []
    context.received_commands = []
    
    # Poll until no more commands (or max attempts to prevent infinite loop)
    max_polling_attempts = 5
    polling_attempt = 0
    
    while polling_attempt < max_polling_attempts:
        polling_attempt += 1
        
        response = context.test_client.get(api_endpoint)
        
        polling_result = {
            "attempt": polling_attempt,
            "response": response,
            "status_code": response.status_code
        }
        
        # Try to get JSON response
        try:
            response_data = response.json()
            polling_result["data"] = response_data
            
            # Check if we got a command
            if response.status_code == 200 and response_data.get("command"):
                context.received_commands.append({
                    "attempt": polling_attempt,
                    "command": response_data["command"],
                    "queue_position": response_data.get("queue_position", 0),
                    "total_queue_size": response_data.get("total_queue_size", 0)
                })
            else:
                # No more commands, break
                break
                
        except ValueError:
            polling_result["data"] = None
            
        context.polling_results.append(polling_result)