def execute(context):
    """Upload files as part of result reporting process"""
    # When: I upload files as part of result reporting
    
    # Prepare the request payload for client result submission with files
    upload_payload = {
        "command_id": context.command_id,
        "execution_status": "completed",
        "result_content": context.test_result_content,
        "result_files": [
            {
                "file_name": "execution.log",
                "file_content_base64": context.log_file_base64,
                "content_type": "text/plain",
                "file_summary": "Execution log with timestamps"
            },
            {
                "file_name": "report.json",
                "file_content_base64": context.report_file_base64,
                "content_type": "application/json", 
                "file_summary": "Execution report with metrics"
            }
        ]
    }
    
    # Send HTTP POST request to upload result with files
    api_url = f"/api/sessions/{context.session_id}/commands/{context.command_id}/result-with-files"
    response = context.test_client.post(api_url, json=upload_payload)
    
    # Store response for verification
    context.upload_response = response
    
    if response.status_code == 200:
        context.upload_data = response.json()