Feature: Non Existent Client Error Handling
  As a server
  I want to reject commands targeting non-existent clients
  So that errors are handled gracefully

  Scenario: Reject command targeting non-existent client
    Given a command targets a non-existent client-id
    When the command is submitted
    Then I should return an appropriate error response
    And the command should not be queued