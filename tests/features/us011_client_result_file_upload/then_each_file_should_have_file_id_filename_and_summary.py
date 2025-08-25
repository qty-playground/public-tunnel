def execute(context):
    """Verify that each uploaded file has file-id, filename, and summary"""
    # Then: each file should have file-id, filename, and summary
    
    # Verify successful upload response
    assert context.upload_response.status_code == 200, (
        f"Expected successful upload (200), got {context.upload_response.status_code}: "
        f"{context.upload_response.text}"
    )
    
    # Verify response structure
    upload_data = context.upload_data
    assert "uploaded_files" in upload_data, "Response should contain 'uploaded_files'"
    assert "file_references" in upload_data, "Response should contain 'file_references'"
    
    uploaded_files = upload_data["uploaded_files"]
    file_references = upload_data["file_references"]
    
    # Verify we have the expected number of files
    assert len(uploaded_files) == 2, f"Expected 2 files, got {len(uploaded_files)}"
    assert len(file_references) == 2, f"Expected 2 file references, got {len(file_references)}"
    
    # Verify each file has required metadata
    for i, file_info in enumerate(uploaded_files):
        expected_file = context.expected_files[i]
        
        # Check required fields exist and are valid
        assert "file_id" in file_info, f"File {i} missing file_id"
        assert "file_name" in file_info, f"File {i} missing file_name"
        assert "file_summary" in file_info, f"File {i} missing file_summary"
        
        # Verify unique file-id (should be non-empty string)
        file_id = file_info["file_id"]
        assert file_id and isinstance(file_id, str), f"File {i} has invalid file_id: {file_id}"
        
        # Verify original filename preserved
        assert file_info["file_name"] == expected_file["file_name"], (
            f"File {i} filename mismatch: expected {expected_file['file_name']}, "
            f"got {file_info['file_name']}"
        )
        
        # Verify descriptive summary exists
        file_summary = file_info["file_summary"]
        assert file_summary and isinstance(file_summary, str), (
            f"File {i} has invalid file_summary: {file_summary}"
        )
        assert file_summary == expected_file["file_summary"], (
            f"File {i} summary mismatch: expected {expected_file['file_summary']}, "
            f"got {file_summary}"
        )
        
        # Verify file-id is in file_references list
        assert file_id in file_references, (
            f"File {i} file_id {file_id} not found in file_references list"
        )
    
    # Store file IDs for next verification step
    context.uploaded_file_ids = [f["file_id"] for f in uploaded_files]