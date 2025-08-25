def execute(context):
    """
    Upload multiple files with the same filename "test.txt" to test unique ID generation
    
    This step:
    1. Creates multiple different files with the same filename
    2. Uploads them to the same session via HTTP API
    3. Stores the upload responses for later verification
    """
    import base64
    
    # Set phase to GIVEN to allow state modification
    context.phase = context.phase.__class__.GIVEN
    
    # Set up test session
    context.test_session_id = "test-session-us022-001"
    context.test_filename = "test.txt"
    
    # Create multiple files with same name but different content
    test_files_data = [
        {
            "name": "test.txt",
            "content": "First file content - Lorem ipsum dolor sit amet",
            "content_type": "text/plain",
            "summary": "First test file for unique ID testing"
        },
        {
            "name": "test.txt", 
            "content": "Second file content - Different content with more text and numbers: 12345",
            "content_type": "text/plain",
            "summary": "Second test file for unique ID testing"
        },
        {
            "name": "test.txt",
            "content": "Third file content - Another unique content with special chars: 中文測試 & symbols!",
            "content_type": "text/plain", 
            "summary": "Third test file for unique ID testing"
        }
    ]
    
    # Initialize response storage
    context.upload_responses = []
    
    # Upload each file via HTTP API (external method)
    for file_data in test_files_data:
        # Encode content to Base64
        file_content_base64 = base64.b64encode(
            file_data["content"].encode('utf-8')
        ).decode('utf-8')
        
        # Prepare upload request
        upload_request = {
            "file_name": file_data["name"],
            "file_content_base64": file_content_base64,
            "content_type": file_data["content_type"],
            "file_summary": file_data["summary"]
        }
        
        # Upload file via HTTP API
        response = context.test_client.post(
            f"/api/sessions/{context.test_session_id}/files",
            json=upload_request
        )
        
        # Store response for later verification
        context.upload_responses.append(response)
        
    # Store expected results for verification
    context.expected_file_count = len(test_files_data)
    context.expected_filename = "test.txt"