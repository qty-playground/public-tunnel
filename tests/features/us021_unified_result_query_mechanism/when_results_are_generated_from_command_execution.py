def execute(context):
    """When step: Query unified results through the API"""
    from conftest import BDDPhase
    
    context.phase = BDDPhase.WHEN
    
    # Try to query fast command result through unified API
    fast_response = context.test_client.get(
        f"/api/sessions/{context.session_id}/results/{context.fast_command_id}"
    )
    context.fast_response = fast_response
    
    # Try to query slow command result through unified API
    slow_response = context.test_client.get(
        f"/api/sessions/{context.session_id}/results/{context.slow_command_id}"
    )
    context.slow_response = slow_response