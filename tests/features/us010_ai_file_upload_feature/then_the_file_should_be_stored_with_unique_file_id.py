def execute(context):
    """
    Verify that file upload was successful and returned unique file-id
    
    This step verifies:
    1. HTTP response status is 200 OK
    2. Response contains unique file-id
    3. Response contains expected file metadata
    4. File is actually stored in the FileManager service
    """
    # Set phase to THEN for read-only verification
    context.phase = context.phase.__class__.THEN
    
    # Verify HTTP response is successful
    assert context.upload_status_code == 200, \
        f"Expected HTTP 200, got {context.upload_status_code}"
    
    # Verify response data exists
    assert context.upload_response_data is not None, \
        "Upload response should contain JSON data"
    
    # Verify file_id is present and non-empty
    assert "file_id" in context.upload_response_data, \
        "Response should contain file_id"
    file_id = context.upload_response_data["file_id"]
    assert file_id and len(file_id.strip()) > 0, \
        "File ID should be non-empty"
    
    # Verify response contains expected metadata
    assert context.upload_response_data["file_name"] == context.test_file_name, \
        f"Expected file_name {context.test_file_name}, got {context.upload_response_data['file_name']}"
    assert context.upload_response_data["session_id"] == context.test_session_id, \
        f"Expected session_id {context.test_session_id}, got {context.upload_response_data['session_id']}"
    assert context.upload_response_data["content_type"] == context.test_content_type, \
        f"Expected content_type {context.test_content_type}, got {context.upload_response_data['content_type']}"
    
    # Verify file size matches original content
    expected_size = len(context.test_file_content.encode('utf-8'))
    actual_size = context.upload_response_data["file_size_bytes"]
    assert actual_size == expected_size, \
        f"Expected file size {expected_size}, got {actual_size}"
    
    # Get file_id for verification (already stored in WHEN phase)
    
    # Verify file exists in FileManager service (internal state check)
    from public_tunnel.dependencies.providers import get_file_manager
    file_manager = get_file_manager()
    assert file_manager.file_exists_in_session(context.test_session_id, file_id), \
        f"File {file_id} should exist in session {context.test_session_id}"