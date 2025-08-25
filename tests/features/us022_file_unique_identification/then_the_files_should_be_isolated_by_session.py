def execute(context):
    """
    Verify that files with same name in different sessions are properly isolated
    
    This step:
    1. Verifies each session returns only its own files
    2. Confirms files with same name have different file-ids across sessions
    3. Ensures session isolation is maintained
    """
    # Set phase to THEN for read-only verification
    context.phase = context.phase.__class__.THEN
    
    session_files_data = {}
    all_file_ids = []
    
    # Collect all file data from both sessions
    for session_id, query_response in context.session_queries.items():
        # Verify successful query
        assert query_response.status_code == 200, \
            f"Session {session_id} query failed with status {query_response.status_code}"
        
        query_data = query_response.json()
        session_files_data[session_id] = query_data
        
        # Verify each session has exactly one file
        assert query_data["total_files"] == 1, \
            f"Expected 1 file in session {session_id}, got {query_data['total_files']}"
        
        file_item = query_data["files"][0]
        all_file_ids.append(file_item["file_id"])
        
        # Verify filename matches what was uploaded
        expected_filename = context.session_uploads[session_id]["filename"]
        assert file_item["file_name"] == expected_filename, \
            f"Expected filename '{expected_filename}' in session {session_id}, got '{file_item['file_name']}'"
    
    # Critical verification: Files in different sessions should have unique file-ids
    # even if they have the same filename
    unique_file_ids = set(all_file_ids)
    assert len(all_file_ids) == len(unique_file_ids), \
        f"Files with same name across sessions should have unique file-ids! Got IDs: {all_file_ids}"
    
    # Verify session isolation: each session should only see its own file
    session_ids = list(context.session_uploads.keys())
    assert len(session_ids) == 2, f"Expected 2 sessions, got {len(session_ids)}"
    
    session1, session2 = session_ids
    
    # Session 1 should only see its file
    session1_files = session_files_data[session1]["files"]
    assert len(session1_files) == 1, f"Session {session1} should see only 1 file"
    
    # Session 2 should only see its file  
    session2_files = session_files_data[session2]["files"]
    assert len(session2_files) == 1, f"Session {session2} should see only 1 file"
    
    # Files should have different IDs even with same name
    file1_id = session1_files[0]["file_id"]
    file2_id = session2_files[0]["file_id"]
    assert file1_id != file2_id, \
        f"Files with same name in different sessions should have unique IDs, got same ID: {file1_id}"
    
    # Successfully verified session isolation