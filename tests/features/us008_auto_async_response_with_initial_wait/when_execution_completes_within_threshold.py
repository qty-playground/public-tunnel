from conftest import BDDPhase
import time

def execute(context):
    """Execute command submission expecting immediate response (fast execution)"""
    context.phase = BDDPhase.WHEN
    
    # Submit command with expectation of immediate response
    # This should use a new API endpoint that supports auto async mode
    submit_response = context.test_client.post(
        f"/api/sessions/{context.session_id}/commands/submit-auto-async",
        json=context.command_submission_data
    )
    
    context.submission_result = {
        "response": submit_response,
        "status_code": submit_response.status_code,
        "response_data": submit_response.json() if submit_response.status_code in [200, 201] else None,
        "submission_time": time.time()
    }