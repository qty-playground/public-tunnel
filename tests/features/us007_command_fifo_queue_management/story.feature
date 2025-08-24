Feature: Command FIFO Queue Management
  As a server
  I want to queue commands in FIFO order
  So that commands are processed fairly

  Scenario: Multiple commands queued for same client are returned in FIFO order
    Given multiple commands are submitted to the same client
    When the client polls for commands
    Then commands should be returned in first-in-first-out order
    And each polling should return only one command