Feature: Client Execution Error Reporting
  As a client
  I want to report execution failures in the same format as success
  So that AI can handle errors consistently

  Scenario: Client reports command execution failure
    Given a command execution fails
    When I report the result
    Then the error should be formatted like a normal result
    And the AI should be able to query the error like any result