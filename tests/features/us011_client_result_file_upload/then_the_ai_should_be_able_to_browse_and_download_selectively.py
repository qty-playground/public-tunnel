import base64

def execute(context):
    """Verify that AI can browse and download files selectively"""
    # And: the AI should be able to browse and download selectively
    
    # Test 1: Browse files in session (using existing file list API)
    list_url = f"/api/sessions/{context.session_id}/files"
    list_response = context.test_client.get(list_url)
    
    assert list_response.status_code == 200, (
        f"Expected successful file list (200), got {list_response.status_code}: "
        f"{list_response.text}"
    )
    
    file_list_data = list_response.json()
    assert "files" in file_list_data, "File list response should contain 'files'"
    
    files_in_session = file_list_data["files"]
    assert len(files_in_session) >= 2, (
        f"Expected at least 2 files in session, got {len(files_in_session)}"
    )
    
    # Verify uploaded files are in the session file list
    session_file_ids = [f["file_id"] for f in files_in_session]
    for file_id in context.uploaded_file_ids:
        assert file_id in session_file_ids, (
            f"Uploaded file {file_id} not found in session file list"
        )
    
    # Test 2: Download files selectively (using existing file download API)
    for i, file_id in enumerate(context.uploaded_file_ids):
        download_url = f"/api/sessions/{context.session_id}/files/{file_id}"
        download_response = context.test_client.get(download_url)
        
        assert download_response.status_code == 200, (
            f"Expected successful file download (200) for file {file_id}, "
            f"got {download_response.status_code}: {download_response.text}"
        )
        
        download_data = download_response.json()
        
        # Verify download response structure
        assert "file_id" in download_data, f"Download response for {file_id} missing file_id"
        assert "file_name" in download_data, f"Download response for {file_id} missing file_name"
        assert "file_content_base64" in download_data, f"Download response for {file_id} missing file_content_base64"
        assert "file_summary" in download_data, f"Download response for {file_id} missing file_summary"
        
        # Verify downloaded content matches uploaded content
        downloaded_content_base64 = download_data["file_content_base64"]
        downloaded_content = base64.b64decode(downloaded_content_base64).decode()
        expected_content = context.expected_files[i]["content"]
        
        assert downloaded_content == expected_content, (
            f"Downloaded content for file {file_id} doesn't match uploaded content. "
            f"Expected: {expected_content}, Got: {downloaded_content}"
        )
        
        # Verify file metadata preserved
        expected_file = context.expected_files[i]
        assert download_data["file_name"] == expected_file["file_name"], (
            f"Downloaded filename mismatch for {file_id}: "
            f"expected {expected_file['file_name']}, got {download_data['file_name']}"
        )
        assert download_data["file_summary"] == expected_file["file_summary"], (
            f"Downloaded summary mismatch for {file_id}: "
            f"expected {expected_file['file_summary']}, got {download_data['file_summary']}"
        )