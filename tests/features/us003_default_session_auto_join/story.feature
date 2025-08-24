Feature: Default Session Auto Join
  As a client
  I want to automatically join default session when no session-id specified
  So that I can start working without manual configuration

  Scenario: Client automatically joins default session on first polling
    Given I start polling without specifying session-id
    When I send my first polling request
    Then I should be automatically assigned to default session
    And my client-id should be recorded in the session