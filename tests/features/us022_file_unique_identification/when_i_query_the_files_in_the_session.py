def execute(context):
    """
    Query files in the current test session to retrieve file list
    
    This step:
    1. Makes HTTP request to list files in the test session
    2. Stores the response for verification in Then steps
    """
    # Set phase to WHEN to allow result collection
    context.phase = context.phase.__class__.WHEN
    
    # Query files via HTTP API (external method only)
    response = context.test_client.get(
        f"/api/sessions/{context.test_session_id}/files"
    )
    
    # Store response for verification
    context.query_response = response