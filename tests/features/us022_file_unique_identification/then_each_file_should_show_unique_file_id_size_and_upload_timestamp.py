def execute(context):
    """
    Verify each file shows unique file-id, size, and upload timestamp for identification
    
    This step:
    1. Verifies metadata query response is successful
    2. Confirms each file has unique identifying characteristics
    3. Validates that metadata can be used to distinguish files
    """
    # Set phase to THEN for read-only verification
    context.phase = context.phase.__class__.THEN
    
    # Verify external state - HTTP response
    assert context.metadata_query_response.status_code == 200, \
        f"Expected 200, got {context.metadata_query_response.status_code}"
    
    query_data = context.metadata_query_response.json()
    
    # Verify correct number of files returned
    assert query_data["total_files"] == context.expected_files_count, \
        f"Expected {context.expected_files_count} files, got {query_data['total_files']}"
    
    files = query_data["files"]
    
    # Verify all files have the same filename (as expected for this test)
    for file_item in files:
        assert file_item["file_name"] == context.test_filename, \
            f"Expected filename '{context.test_filename}', got '{file_item['file_name']}'"
    
    # Critical verification 1: Each file should have a unique file-id
    file_ids = [file_item["file_id"] for file_item in files]
    unique_file_ids = set(file_ids)
    assert len(file_ids) == len(unique_file_ids), \
        f"Found duplicate file IDs! Expected {len(file_ids)} unique IDs, got {len(unique_file_ids)}. IDs: {file_ids}"
    
    # Critical verification 2: Each file should have different sizes
    file_sizes = [file_item["file_size_bytes"] for file_item in files]
    unique_sizes = set(file_sizes)
    assert len(file_sizes) == len(unique_sizes), \
        f"Expected unique file sizes for distinction, got sizes: {file_sizes}"
    
    # Critical verification 3: Each file should have different upload timestamps
    upload_timestamps = [file_item["upload_timestamp"] for file_item in files]
    unique_timestamps = set(upload_timestamps)
    assert len(upload_timestamps) == len(unique_timestamps), \
        f"Expected unique upload timestamps for distinction, got timestamps: {upload_timestamps}"
    
    # Verification 4: Each file should have different summaries
    file_summaries = [file_item.get("file_summary", "") for file_item in files]
    unique_summaries = set(file_summaries)
    assert len(file_summaries) == len(unique_summaries), \
        f"Expected unique file summaries for distinction, got summaries: {file_summaries}"
    
    # All files with identical names have unique metadata
    # Each file has unique ID, size, and timestamp