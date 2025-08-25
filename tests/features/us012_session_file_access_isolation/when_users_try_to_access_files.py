def execute(context):
    """
    Attempt file access scenarios to test session isolation
    
    This step performs the actual API calls to test:
    1. Same session file access (should work)
    2. Cross-session file access (should be blocked)
    3. US-012 specific isolation validation
    """
    from conftest import BDDPhase
    
    # Set phase to WHEN for action execution
    context.phase = BDDPhase.WHEN
    
    # Test scenario 1: Session A tries to access its own file (should succeed)
    context.same_session_access_response = context.test_client.get(
        f"/api/sessions/{context.session_a_id}/files/{context.file_a_id}"
    )
    
    # Test scenario 2: Session A tries to access Session B's file (should be blocked)
    context.cross_session_access_response = context.test_client.get(
        f"/api/sessions/{context.session_a_id}/files/{context.file_b_id}"
    )
    
    # Test scenario 3: Use US-012 validation endpoint to check access permissions
    context.access_validation_same_session_response = context.test_client.post(
        f"/api/sessions/{context.session_a_id}/files/{context.file_a_id}/validate-access"
    )
    
    context.access_validation_cross_session_response = context.test_client.post(
        f"/api/sessions/{context.session_a_id}/files/{context.file_b_id}/validate-access"
    )
    
    # Test scenario 4: Use US-012 secure download endpoint
    context.secure_download_same_session_response = context.test_client.get(
        f"/api/sessions/{context.session_a_id}/files/{context.file_a_id}/secure-download"
    )
    
    context.secure_download_cross_session_response = context.test_client.get(
        f"/api/sessions/{context.session_a_id}/files/{context.file_b_id}/secure-download"
    )
    
    # Store all responses for verification in subsequent steps
    context.access_test_responses = {
        "same_session_access": context.same_session_access_response,
        "cross_session_access": context.cross_session_access_response,
        "validation_same_session": context.access_validation_same_session_response,
        "validation_cross_session": context.access_validation_cross_session_response,
        "secure_download_same": context.secure_download_same_session_response,
        "secure_download_cross": context.secure_download_cross_session_response
    }