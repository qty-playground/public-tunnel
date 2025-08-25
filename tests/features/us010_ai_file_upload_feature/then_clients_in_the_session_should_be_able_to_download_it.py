def execute(context):
    """
    Verify that clients can download the uploaded file via API
    
    This step verifies:
    1. File can be downloaded using file-id
    2. Downloaded content matches original
    3. File listing API shows the uploaded file
    """
    # Continue in THEN phase for read-only verification
    # (Already set in previous step)
    
    # Test file download API
    download_endpoint = f"/api/sessions/{context.test_session_id}/files/{context.uploaded_file_id}"
    download_response = context.test_client.get(download_endpoint)
    
    # Verify download response is successful
    assert download_response.status_code == 200, \
        f"Expected download HTTP 200, got {download_response.status_code}"
    
    download_data = download_response.json()
    assert download_data is not None, "Download response should contain JSON data"
    
    # Verify downloaded file metadata matches upload
    assert download_data["file_id"] == context.uploaded_file_id, \
        f"Expected file_id {context.uploaded_file_id}, got {download_data['file_id']}"
    assert download_data["file_name"] == context.test_file_name, \
        f"Expected file_name {context.test_file_name}, got {download_data['file_name']}"
    assert download_data["content_type"] == context.test_content_type, \
        f"Expected content_type {context.test_content_type}, got {download_data['content_type']}"
    
    # Verify downloaded content matches original (Base64 decoded)
    import base64
    downloaded_content_bytes = base64.b64decode(download_data["file_content_base64"])
    downloaded_content = downloaded_content_bytes.decode('utf-8')
    assert downloaded_content == context.test_file_content, \
        f"Downloaded content does not match original. Expected: {context.test_file_content}, Got: {downloaded_content}"
    
    # Test file listing API
    list_endpoint = f"/api/sessions/{context.test_session_id}/files"
    list_response = context.test_client.get(list_endpoint)
    
    # Verify listing response is successful
    assert list_response.status_code == 200, \
        f"Expected listing HTTP 200, got {list_response.status_code}"
    
    list_data = list_response.json()
    assert list_data is not None, "Listing response should contain JSON data"
    
    # Verify uploaded file appears in listing
    assert list_data["session_id"] == context.test_session_id, \
        f"Expected session_id {context.test_session_id}, got {list_data['session_id']}"
    assert list_data["total_files"] >= 1, \
        f"Expected at least 1 file in session, got {list_data['total_files']}"
    
    # Find uploaded file in list
    uploaded_file_found = False
    for file_metadata in list_data["files"]:
        if file_metadata["file_id"] == context.uploaded_file_id:
            uploaded_file_found = True
            assert file_metadata["file_name"] == context.test_file_name, \
                f"Listed file name mismatch: expected {context.test_file_name}, got {file_metadata['file_name']}"
            break
    
    assert uploaded_file_found, \
        f"Uploaded file {context.uploaded_file_id} should appear in session file listing"