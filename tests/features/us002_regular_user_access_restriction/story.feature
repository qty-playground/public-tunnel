Feature: Regular User Access Restriction
  As a regular user
  I want to be denied when trying to list all sessions
  So that system security is maintained

  Scenario: Regular user denied access without admin token
    Given I don't have a valid admin token
    When I query GET /api/sessions
    Then I should receive a 403 Forbidden response
    And I should not see any session information

  Scenario: Regular user denied access with invalid admin token  
    Given I have an invalid admin token
    When I query GET /api/sessions with invalid token
    Then I should receive a 403 Forbidden response
    And I should not see any session information