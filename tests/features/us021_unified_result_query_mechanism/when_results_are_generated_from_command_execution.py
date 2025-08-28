def execute(context):
    """When step: Query results from both sync and async commands through the unified API"""
    from conftest import BDDPhase
    
    context.phase = BDDPhase.WHEN
    
    # Query sync command result through unified API
    # This command had immediate execution (sync mode)
    sync_query_response = context.test_client.get(
        f"/api/sessions/{context.session_id}/results/{context.sync_command_id}"
    )
    context.sync_query_response = sync_query_response
    
    # Query async command result through unified API  
    # This command was submitted for async execution
    async_query_response = context.test_client.get(
        f"/api/sessions/{context.session_id}/results/{context.async_command_id}"
    )
    context.async_query_response = async_query_response