def execute(context):
    """When step: Client reports the execution failure result to the server"""
    from conftest import BDDPhase
    from public_tunnel.models.execution_result import ExecutionResultSubmissionRequest, ExecutionResultStatus
    
    context.phase = BDDPhase.WHEN
    
    # Create error result submission request
    error_request = ExecutionResultSubmissionRequest(
        command_id=context.command_id,
        execution_status=ExecutionResultStatus.FAILED,
        result_content=context.result_content,  # Should be None for failed commands
        error_message=context.error_message,
        execution_duration_seconds=context.execution_duration,
        file_references=None  # No file references for failed commands
    )
    
    # Report the error result via API
    response = context.test_client.post(
        f"/api/sessions/{context.session_id}/commands/{context.command_id}/error",
        json=error_request.model_dump()
    )
    context.error_report_response = response
    
    # Also query the error result through unified API (for AI query verification in Then step)
    query_response = context.test_client.get(
        f"/api/sessions/{context.session_id}/commands/{context.command_id}/error"
    )
    context.error_query_response = query_response