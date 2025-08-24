Feature: Unified Result Query Mechanism
  As a server
  I want to handle both sync and async commands through the same result mechanism
  So that result management is consistent

  Scenario: Both sync and async commands results are stored with command-id indexing
    Given commands in both sync and async modes are submitted
    When results are generated from command execution
    Then all results should be stored with command-id indexing
    And results should be queryable through the same API