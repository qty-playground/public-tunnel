def execute(context, filename, session_id):
    """
    Upload a file with specific filename to specific session
    
    Args:
        context: Test context
        filename: Name of the file to upload
        session_id: Target session ID
    
    This step uploads a file and stores the response for later verification.
    """
    import base64
    
    # Set phase to GIVEN to allow state modification
    context.phase = context.phase.__class__.GIVEN
    
    # Initialize sessions storage if not exists
    if not hasattr(context, 'session_uploads'):
        context.session_uploads = {}
    
    # Create file content based on session to make them different
    file_content = f"File content for {filename} in {session_id}. This content is unique to this session and file combination."
    
    # Encode content to Base64
    file_content_base64 = base64.b64encode(
        file_content.encode('utf-8')
    ).decode('utf-8')
    
    # Prepare upload request
    upload_request = {
        "file_name": filename,
        "file_content_base64": file_content_base64,
        "content_type": "application/json",
        "file_summary": f"Test file {filename} for session {session_id}"
    }
    
    # Upload file via HTTP API
    response = context.test_client.post(
        f"/api/sessions/{session_id}/files",
        json=upload_request
    )
    
    # Store response by session for later verification
    context.session_uploads[session_id] = {
        "filename": filename,
        "upload_response": response,
        "upload_request": upload_request
    }