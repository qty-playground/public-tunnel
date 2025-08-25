Feature: Specified Session Collaboration Mode
  As a client
  I want to join existing session when session-id is specified
  So that I can collaborate with other clients

  Scenario: Client joins existing session by specifying session-id
    Given there is an existing session with specified session-id
    When I start polling with that session-id
    Then I should join the existing session
    And I should be able to see other clients in the same session