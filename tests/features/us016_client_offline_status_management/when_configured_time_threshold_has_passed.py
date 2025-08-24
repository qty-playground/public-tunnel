from conftest import BDDPhase
import time

def execute(context):
    """Simulate the configured time threshold passing since the client's last_seen"""
    context.phase = BDDPhase.WHEN
    
    # Step 1: Wait for the configured threshold time to pass
    # We wait slightly longer than the threshold to ensure the client is considered offline
    threshold_seconds = getattr(context, 'offline_threshold_seconds', 2)
    sleep_time = threshold_seconds + 1  # Wait a bit longer than the threshold
    
    time.sleep(sleep_time)  # Wait for threshold to pass
    
    # Step 2: Trigger the server's offline detection mechanism using HTTP API
    # We use the force offline check API to simulate the server's periodic check
    force_check_response = context.test_client.post(
        f"/api/sessions/{context.session_id}/clients/force-offline-check",
        json={"session_id": context.session_id}
    )
    
    # Store the response for Then step verification
    context.force_check_response = force_check_response
    context.force_check_timestamp = time.time()