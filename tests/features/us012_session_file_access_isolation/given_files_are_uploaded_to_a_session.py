def execute(context):
    """
    Set up test scenario with files uploaded to different sessions
    
    This step prepares the test environment by:
    1. Creating two different sessions
    2. Uploading files to each session
    3. Storing session and file information for later validation
    """
    from conftest import BDDPhase
    import base64
    
    # Set phase to GIVEN for setup operations
    context.phase = BDDPhase.GIVEN
    
    # Prepare test data for two separate sessions
    context.session_a_id = "test-session-a-us012"
    context.session_b_id = "test-session-b-us012"
    
    # Test file content for session A
    context.file_a_name = "session-a-file.txt"
    context.file_a_content = "This file belongs to session A - US-012 test"
    context.file_a_content_base64 = base64.b64encode(context.file_a_content.encode()).decode()
    
    # Test file content for session B  
    context.file_b_name = "session-b-file.txt"
    context.file_b_content = "This file belongs to session B - US-012 test"
    context.file_b_content_base64 = base64.b64encode(context.file_b_content.encode()).decode()
    
    # Upload file to session A
    upload_request_a = {
        "file_name": context.file_a_name,
        "file_content_base64": context.file_a_content_base64,
        "content_type": "text/plain",
        "file_summary": "US-012 test file for session A"
    }
    
    response_a = context.test_client.post(
        f"/api/sessions/{context.session_a_id}/files",
        json=upload_request_a
    )
    
    # Store session A file information
    if response_a.status_code == 200:
        context.file_a_id = response_a.json().get("file_id")
        context.file_a_uploaded = True
    else:
        context.file_a_uploaded = False
        context.file_a_id = "mock-file-a-id"  # Mock for validation tests
    
    # Upload file to session B
    upload_request_b = {
        "file_name": context.file_b_name,
        "file_content_base64": context.file_b_content_base64,
        "content_type": "text/plain", 
        "file_summary": "US-012 test file for session B"
    }
    
    response_b = context.test_client.post(
        f"/api/sessions/{context.session_b_id}/files",
        json=upload_request_b
    )
    
    # Store session B file information
    if response_b.status_code == 200:
        context.file_b_id = response_b.json().get("file_id")
        context.file_b_uploaded = True
    else:
        context.file_b_uploaded = False
        context.file_b_id = "mock-file-b-id"  # Mock for validation tests
    
    # Store upload responses for later verification
    context.upload_response_a = response_a
    context.upload_response_b = response_b