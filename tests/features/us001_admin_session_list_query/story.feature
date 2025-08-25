Feature: Admin Session List Query
  As an admin user
  I want to list all sessions with valid token
  So that I can manage the entire system

  Scenario: Admin queries all sessions successfully
    Given I have a valid admin token
    And there are multiple sessions in the system
    When I query GET /api/sessions with admin token
    Then I should receive a list of all sessions
    And each session should include basic metadata

  Scenario: Admin queries all sessions when only default session exists
    Given I have a valid admin token
    And there are no sessions in the system
    When I query GET /api/sessions with admin token
    Then I should receive an empty session list
    And the response status should be success