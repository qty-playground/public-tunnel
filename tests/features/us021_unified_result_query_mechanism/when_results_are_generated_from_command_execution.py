def execute(context):
    """When step: Query unified results through the API"""
    from conftest import BDDPhase
    
    context.phase = BDDPhase.WHEN
    
    # Try to query sync command result through unified API
    sync_response = context.test_client.get(
        f"/api/sessions/{context.session_id}/results/{context.sync_command_id}"
    )
    context.sync_response = sync_response
    
    # Try to query async command result through unified API
    async_response = context.test_client.get(
        f"/api/sessions/{context.session_id}/results/{context.async_command_id}"
    )
    context.async_response = async_response