def execute(context):
    """
    Verify that all uploaded files have unique file-ids
    
    This step:
    1. Checks that query response is successful
    2. Verifies all uploaded files are returned
    3. Ensures each file has a unique file-id
    """
    # Set phase to THEN for read-only verification
    context.phase = context.phase.__class__.THEN
    
    all_file_ids = []
    
    # Handle different data structures from different scenarios
    if hasattr(context, 'query_response'):
        # Scenario 1: Single session with multiple files of same name
        assert context.query_response.status_code == 200, f"Expected 200, got {context.query_response.status_code}"
        
        query_data = context.query_response.json()
        
        # Verify correct number of files returned
        assert query_data["total_files"] == context.expected_file_count, \
            f"Expected {context.expected_file_count} files, got {query_data['total_files']}"
        
        # Verify all files have the same filename (as expected)
        files = query_data["files"]
        for file_item in files:
            assert file_item["file_name"] == context.expected_filename, \
                f"Expected filename '{context.expected_filename}', got '{file_item['file_name']}'"
        
        # Collect file IDs
        all_file_ids = [file_item["file_id"] for file_item in files]
        
    elif hasattr(context, 'session_queries'):
        # Scenario 2: Multiple sessions with files of same name
        for session_id, query_response in context.session_queries.items():
            assert query_response.status_code == 200, f"Session {session_id} query failed with status {query_response.status_code}"
            
            query_data = query_response.json()
            files = query_data["files"]
            
            # Collect file IDs from all sessions
            for file_item in files:
                all_file_ids.append(file_item["file_id"])
                
    elif hasattr(context, 'metadata_query_response'):
        # Scenario 3: Files with identical names but different content for metadata testing
        assert context.metadata_query_response.status_code == 200, f"Expected 200, got {context.metadata_query_response.status_code}"
        
        query_data = context.metadata_query_response.json()
        files = query_data["files"]
        
        # Collect file IDs
        all_file_ids = [file_item["file_id"] for file_item in files]
    
    else:
        raise AssertionError("No valid query data found in context")
    
    # Critical verification: Each file should have a unique file-id
    unique_file_ids = set(all_file_ids)
    
    assert len(all_file_ids) == len(unique_file_ids), \
        f"Found duplicate file IDs! Expected {len(all_file_ids)} unique IDs, got {len(unique_file_ids)}. IDs: {all_file_ids}"