Feature: Targeted Client Command Submission
  As an AI assistant
  I want to submit commands to specific clients
  So that tasks are executed on target machines

  Scenario: Submit command to valid target client
    Given I have a valid target client-id
    When I submit a command with target_client specified
    Then the command should be queued for that specific client
    And only that client should receive the command