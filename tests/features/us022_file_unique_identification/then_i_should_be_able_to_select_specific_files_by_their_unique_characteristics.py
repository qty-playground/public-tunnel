def execute(context):
    """
    Verify ability to select specific files by their unique characteristics
    
    This step:
    1. Demonstrates file selection by file-id
    2. Shows how metadata can be used for file identification
    3. Validates practical usage of unique identification
    """
    # Set phase to THEN for read-only verification
    context.phase = context.phase.__class__.THEN
    
    # Get files from metadata query response (read-only access)
    query_data = context.metadata_query_response.json()
    files = query_data["files"]
    
    # Demonstrate file selection by different characteristics
    
    # 1. Selection by file-id (most direct method)
    for file_item in files:
        file_id = file_item["file_id"]
        
        # Test downloading file by unique ID
        download_response = context.test_client.get(
            f"/api/sessions/{context.test_session_id}/files/{file_id}"
        )
        
        assert download_response.status_code == 200, \
            f"Failed to download file with ID {file_id}: {download_response.status_code}"
        
        download_data = download_response.json()
        assert download_data["file_id"] == file_id, \
            f"Downloaded file ID mismatch: expected {file_id}, got {download_data['file_id']}"
        assert download_data["file_name"] == context.test_filename, \
            f"Downloaded filename mismatch: expected {context.test_filename}, got {download_data['file_name']}"
    
    # 2. Demonstrate selection by size (smallest file)
    files_by_size = sorted(files, key=lambda f: f["file_size_bytes"])
    smallest_file = files_by_size[0]
    largest_file = files_by_size[-1]
    
    # Verify we can identify and select based on size
    assert smallest_file["file_size_bytes"] < largest_file["file_size_bytes"], \
        "Should be able to distinguish files by size"
    
    # 3. Demonstrate selection by summary content
    files_by_summary = {f["file_summary"]: f for f in files}
    
    # Should be able to find specific files by their summary
    small_file_candidates = [f for f in files if "Small" in f.get("file_summary", "")]
    large_file_candidates = [f for f in files if "Large" in f.get("file_summary", "")]
    
    assert len(small_file_candidates) >= 1, "Should be able to find files by summary content"
    assert len(large_file_candidates) >= 1, "Should be able to find files by summary content"
    
    # 4. Demonstrate selection by combination of characteristics
    # Find the file with smallest size AND specific summary pattern
    small_files_with_summary = [
        f for f in files 
        if f["file_size_bytes"] < 50 and "Small" in f.get("file_summary", "")
    ]
    
    assert len(small_files_with_summary) >= 1, \
        "Should be able to select files by combining multiple characteristics"
    
    selected_file = small_files_with_summary[0]
    
    # Verify the selection is meaningful and unique
    assert selected_file["file_name"] == context.test_filename, \
        "Selected file should have the expected filename"
    assert selected_file["file_id"] in [f["file_id"] for f in files], \
        "Selected file should be from the uploaded set"
    
    # Successfully demonstrated file selection methods
    # Files with identical names can be reliably distinguished and selected using metadata