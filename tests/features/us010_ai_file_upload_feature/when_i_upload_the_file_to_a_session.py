def execute(context):
    """
    Send file upload request via US-010 API endpoint
    
    This step performs the actual API call to the US-010 file upload endpoint
    and captures the response for verification.
    """
    # Set phase to WHEN to allow result collection
    context.phase = context.phase.__class__.WHEN
    
    # Use the test client from pytest setup to make API call
    api_endpoint = f"/api/sessions/{context.test_session_id}/files"
    
    # Send POST request with file upload data
    response = context.test_client.post(
        api_endpoint, 
        json=context.file_upload_request
    )
    
    # Store response for verification in subsequent steps
    context.upload_response = response
    context.upload_response_data = response.json() if response.status_code == 200 else None
    context.upload_status_code = response.status_code
    
    # If successful, store the file_id for download verification
    if context.upload_response_data:
        context.uploaded_file_id = context.upload_response_data.get("file_id")