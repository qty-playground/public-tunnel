def execute(context):
    """
    Query files from both test sessions to verify isolation and unique identification
    
    This step:
    1. Makes HTTP requests to list files from each session
    2. Stores responses for verification in Then steps
    """
    # Set phase to WHEN to allow result collection
    context.phase = context.phase.__class__.WHEN
    
    # Query files from each session
    context.session_queries = {}
    
    for session_id in context.session_uploads.keys():
        response = context.test_client.get(
            f"/api/sessions/{session_id}/files"
        )
        context.session_queries[session_id] = response