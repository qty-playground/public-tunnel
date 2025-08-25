"""
Admin Token Validator service for US-001: Admin Session List Query

Provides token validation for admin-level operations.
Follows the centralized dependency injection pattern.
"""

from typing import Optional


class AdminTokenValidator:
    """
    Validates admin tokens against configured admin token from environment.
    
    This service implements the simple token-based authentication mechanism
    described in the OOA design for admin-level operations.
    
    Attributes:
        admin_token: The configured admin token from environment variable
    """
    
    def __init__(self, admin_token: str) -> None:
        """
        Initialize admin token validator with configured token.
        
        Args:
            admin_token: The admin token from environment variable
        """
        self.admin_token = admin_token
    
    def validate_admin_token(self, provided_token: Optional[str]) -> bool:
        """
        Validate provided token against configured admin token.
        
        Args:
            provided_token: Token provided by the client
            
        Returns:
            bool: True if token is valid, False otherwise
        """
        if not provided_token:
            return False
        
        return provided_token == self.admin_token
    
    def is_admin_request(self, token: Optional[str]) -> bool:
        """
        Check if request has valid admin authorization.
        
        Args:
            token: Authorization token from request
            
        Returns:
            bool: True if request is authorized as admin
        """
        return self.validate_admin_token(token)