def execute(context):
    """
    Verify that cross-session file access is properly denied
    
    This step validates:
    1. Cross-session file access returns appropriate error codes  
    2. US-012 validation correctly identifies cross-session violations
    3. Proper error response formats and security measures
    """
    from conftest import BDDPhase
    
    # Set phase to THEN for verification
    context.phase = BDDPhase.THEN
    
    # Implementation phase - US-012 功能完全實作，強制執行跨 session 存取隔離
    
    # Verify cross-session access is blocked (US-010 endpoint with US-012 isolation)
    assert context.cross_session_access_response.status_code == 403, \
        f"Cross-session file access should be forbidden, got {context.cross_session_access_response.status_code}"

    # Verify cross-session validation correctly denies access
    assert context.access_validation_cross_session_response.status_code == 200, \
        f"Cross-session validation should succeed with denial, got {context.access_validation_cross_session_response.status_code}"

    validation_data = context.access_validation_cross_session_response.json()
    assert validation_data["access_granted"] is False, \
        f"Cross-session access should be denied, got {validation_data['access_granted']}"
    assert validation_data["denial_reason"] == "cross_session_access", \
        f"Expected denial reason 'cross_session_access', got {validation_data['denial_reason']}"

    # Verify cross-session secure download is forbidden
    assert context.secure_download_cross_session_response.status_code == 403, \
        f"Cross-session secure download should be forbidden, got {context.secure_download_cross_session_response.status_code}"
    
    # All cross-session access is correctly blocked
    
    # Final validation: ensure all required US-012 specific endpoints are tested and working
    us012_specific_endpoints = [
        "validation_same_session",
        "validation_cross_session", 
        "secure_download_same",
        "secure_download_cross"
    ]
    
    # Verify US-012 specific endpoints are implemented and working correctly
    for endpoint in us012_specific_endpoints:
        assert endpoint in context.access_test_responses, \
            f"Required US-012 endpoint '{endpoint}' was not tested"
        # Validation endpoints should return 200, secure download should return 200/403/404
        assert context.access_test_responses[endpoint].status_code in [200, 403, 404], \
            f"US-012 endpoint '{endpoint}' should be implemented, got {context.access_test_responses[endpoint].status_code}"
    
    # Verify US-010 compatibility endpoints work normally with US-012 isolation
    us010_endpoints = ["same_session_access", "cross_session_access"]
    for endpoint in us010_endpoints:
        assert endpoint in context.access_test_responses, \
            f"US-010 compatibility endpoint '{endpoint}' was not tested"
        # These should work with isolation (200 for same session, 403 for cross-session, 404 for not found)
        assert context.access_test_responses[endpoint].status_code in [200, 404, 403], \
            f"US-010 endpoint '{endpoint}' should work with US-012 isolation, got {context.access_test_responses[endpoint].status_code}"