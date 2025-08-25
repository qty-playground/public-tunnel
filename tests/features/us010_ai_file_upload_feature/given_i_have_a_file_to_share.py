def execute(context):
    """
    Set up test context with a file ready to be shared
    
    This step prepares the test environment by:
    1. Creating test file content
    2. Encoding to Base64 for API compatibility
    3. Setting up test session ID
    4. Storing the test data in context for later use
    """
    import base64
    
    # Set phase to GIVEN to allow state modification
    context.phase = context.phase.__class__.GIVEN
    
    # Set up test data
    context.test_session_id = "test-session-file-upload-001"
    context.test_file_name = "test-document.txt"
    context.test_file_content = "This is a test file content for US-010 file upload feature.\nIt contains multiple lines.\nAnd special characters: 中文測試 & symbols!"
    context.test_content_type = "text/plain"
    context.test_file_summary = "Test file for BDD scenario validation"
    
    # Encode file content to Base64 for API compatibility
    context.test_file_content_base64 = base64.b64encode(
        context.test_file_content.encode('utf-8')
    ).decode('utf-8')
    
    # Prepare file upload request data
    context.file_upload_request = {
        "file_name": context.test_file_name,
        "file_content_base64": context.test_file_content_base64,
        "content_type": context.test_content_type,
        "file_summary": context.test_file_summary
    }