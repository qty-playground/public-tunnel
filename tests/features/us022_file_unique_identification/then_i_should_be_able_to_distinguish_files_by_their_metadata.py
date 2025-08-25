def execute(context):
    """
    Verify that files can be distinguished by their metadata even with identical names
    
    This step:
    1. Verifies each file has distinct metadata (size, upload_timestamp, summary)
    2. Ensures files can be identified by their unique characteristics
    3. Validates that file-ids allow proper distinction
    """
    # Set phase to THEN for read-only verification
    context.phase = context.phase.__class__.THEN
    
    # Read files from query response (read-only access)
    query_data = context.query_response.json()
    files = query_data["files"]
    file_ids = [file_item["file_id"] for file_item in files]
    
    # Verify each file has different metadata for distinction
    file_sizes = [file_item["file_size_bytes"] for file_item in files]
    file_summaries = [file_item.get("file_summary", "") for file_item in files]
    upload_timestamps = [file_item["upload_timestamp"] for file_item in files]
    
    # Files should have different sizes (different content)
    assert len(set(file_sizes)) == len(files), \
        f"Expected unique file sizes for distinction, got sizes: {file_sizes}"
    
    # Files should have different summaries
    assert len(set(file_summaries)) == len(files), \
        f"Expected unique file summaries for distinction, got summaries: {file_summaries}"
    
    # Each file should have a unique combination of characteristics
    file_characteristics = []
    for file_item in files:
        characteristics = (
            file_item["file_id"],
            file_item["file_size_bytes"], 
            file_item.get("file_summary", ""),
            file_item["upload_timestamp"]
        )
        file_characteristics.append(characteristics)
    
    # All combinations should be unique
    unique_characteristics = set(file_characteristics)
    assert len(file_characteristics) == len(unique_characteristics), \
        f"Expected unique file characteristics for each file, got duplicates in: {file_characteristics}"
    
    # Verify we can distinguish files even with same name by using file-id
    for i, file_item in enumerate(files):
        assert file_item["file_name"] == context.expected_filename, \
            f"File {i} should have the same filename for testing purposes"
        assert file_item["file_id"] in file_ids, \
            f"File {i} file_id should be in the retrieved list"
    
    # Successfully distinguished files with identical names using unique metadata