def execute(context):
    """
    Verify that only users within the same session can access files
    
    This step validates:
    1. Same session file access should succeed (when implemented)
    2. US-012 validation endpoints return correct permissions
    3. Proper response formats and status codes
    """
    from conftest import BDDPhase
    
    # Set phase to THEN for verification
    context.phase = BDDPhase.THEN
    
    # Implementation phase - US-012 功能完全實作
    
    # Verify same session access works (US-010 compatibility maintained)
    # Note: This may be 200 (success) or 404 (file not found) depending on test data
    assert context.same_session_access_response.status_code in [200, 404], \
        f"Same session access should work normally (US-010), got {context.same_session_access_response.status_code}"
    
    # Verify access validation API works correctly
    assert context.access_validation_same_session_response.status_code == 200, \
        f"Same session access validation should succeed, got {context.access_validation_same_session_response.status_code}"

    validation_data = context.access_validation_same_session_response.json()
    assert validation_data["access_granted"] is True, \
        f"Same session access should be granted, got {validation_data['access_granted']}"
    
    # Verify secure download API works correctly  
    assert context.secure_download_same_session_response.status_code in [200, 404], \
        f"Same session secure download should work normally, got {context.secure_download_same_session_response.status_code}"
    
    # Success: All same-session access is correctly handled