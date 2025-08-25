Feature: Unified Result Query Mechanism
  As a server
  I want to handle all commands through the same result mechanism
  So that result management is consistent

  Scenario: All command results are stored with command-id indexing
    Given commands are submitted (with automatic timeout handling)
    When results are generated from command execution
    Then all results should be stored with command-id indexing
    And results should be queryable through the same API regardless of execution time