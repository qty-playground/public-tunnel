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
    
    # 確認錯誤訊息包含 client 不存在或未註冊的資訊
    error_detail = response_data["detail"]
    client_not_available_keywords = [
        "not found", "does not exist", "not registered", "has not registered"
    ]
    
    assert any(keyword in error_detail.lower() for keyword in client_not_available_keywords), (
        f"Error should mention client is not available (not found/not registered), got: {error_detail}"
    )
    assert context.non_existent_client_id in error_detail, (
        f"Error should mention the specific client ID '{context.non_existent_client_id}', got: {error_detail}"
    )