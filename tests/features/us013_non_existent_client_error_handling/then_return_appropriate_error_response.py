def execute(context):
    """Then step: 驗證回傳適當的錯誤回應"""
    from conftest import BDDPhase
    
    context.phase = BDDPhase.THEN
    
    # Phase 3: 實際功能實作 - 檢查 404 錯誤  
    assert context.response.status_code == 404, (
        f"Expected 404 Not Found for non-existent client, got {context.response.status_code}"
    )
    
    response_data = context.response.json()
    assert "detail" in response_data, "Error response should contain detail message"
    
    # 驗證確切的錯誤訊息格式（精確比對，不使用模糊檢查）
    error_detail = response_data["detail"]
    expected_error = f"Client '{context.non_existent_client_id}' has not registered in session '{context.session_id}'. Clients must perform at least one polling request before receiving commands."
    
    assert error_detail == expected_error, (
        f"Error message should be exactly: '{expected_error}'\n"
        f"But got: '{error_detail}'"
    )