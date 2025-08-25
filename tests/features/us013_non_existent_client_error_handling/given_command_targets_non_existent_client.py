def execute(context):
    """Given step: 設定一個針對不存在 client 的指令"""
    from conftest import BDDPhase
    
    context.phase = BDDPhase.GIVEN
    
    # 設定測試數據：使用一個肯定不存在的 client ID
    context.non_existent_client_id = "non-existent-client-12345"
    context.command_content = "echo 'test command for non-existent client'"
    context.session_id = "default"  # 使用 default session
    
    # 確保沒有任何 client 被註冊到這個 session
    # 這樣 non_existent_client_id 就真的不存在