Feature: Offline Client Command Rejection
  As a server
  I want to reject commands targeting offline clients
  So that commands don't get lost

  Scenario: Reject command targeting offline client
    Given a client is marked as offline
    When a command targets that client
    Then I should return an error indicating client is offline
    And the command should not be queued