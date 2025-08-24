Feature: Client Offline Status Management
  As a server
  I want to mark clients offline after configured threshold of no polling
  So that system state reflects reality

  Scenario: Client is marked offline after polling timeout
    Given a client has stopped polling
    When the configured time threshold has passed since last_seen
    Then the client should be marked as offline
    And the client should not receive new commands