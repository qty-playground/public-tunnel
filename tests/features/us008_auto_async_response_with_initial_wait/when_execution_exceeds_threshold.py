from conftest import BDDPhase
import time

def execute(context):
    """Execute command submission expecting async response (slow execution)"""
    context.phase = BDDPhase.WHEN
    
    # Modify command to simulate slower execution
    context.command_submission_data["command_content"] = "sleep 2 && echo 'slow command'"
    
    # Submit command with expectation of async response
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