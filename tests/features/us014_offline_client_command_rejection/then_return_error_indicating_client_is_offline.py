def execute(context):
    """Then step: 驗證回傳錯誤指出 client 為 offline 狀態"""
    from conftest import BDDPhase
    
    context.phase = BDDPhase.THEN
    
    # 檢查 HTTP 422 錯誤狀態碼（Unprocessable Entity）
    assert context.response.status_code == 422, (
        f"Expected 422 Unprocessable Entity for offline client, got {context.response.status_code}"
    )
    
    response_data = context.response.json()
    assert "detail" in response_data, "Error response should contain detail message"
    
    # 確認錯誤訊息包含 offline 相關的資訊
    error_detail = response_data["detail"]
    offline_keywords = [
        "offline", "not online", "unavailable", "cannot receive commands"
    ]
    
    assert any(keyword in error_detail.lower() for keyword in offline_keywords), (
        f"Error should mention client is offline, got: {error_detail}"
    )
    
    # 確認錯誤訊息包含特定的 client ID
    assert context.offline_client_id in error_detail, (
        f"Error should mention the specific client ID '{context.offline_client_id}', got: {error_detail}"
    )
    
    # 確認錯誤訊息提到了防止指令遺失的原因
    command_loss_prevention_keywords = [
        "command loss", "prevent", "lost", "rejected"
    ]
    
    assert any(keyword in error_detail.lower() for keyword in command_loss_prevention_keywords), (
        f"Error should mention command loss prevention, got: {error_detail}"
    )